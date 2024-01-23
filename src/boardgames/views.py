from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    TemplateView,
    View,
)

from .models import BoardGame, GameRequest
from .bgg_api import BGGSearch, BGGItemDetails
from .forms import GameRequestForm, RequestAcceptForm

from icecream import ic


class BrowseBoardgamesView(LoginRequiredMixin, ListView):
    template_name = 'boardgames/browse_games.html'
    context_object_name = 'boardgames'
    model = BoardGame
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get('name')
        queryset = BoardGame.objects.filter(
                status=BoardGame.Status.SUPPORTED,
            )

        if name:
            queryset = queryset.filter(
                primary_name__icontains=name,
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', '')
        return context


class RequestBoardgamesView(LoginRequiredMixin, ListView):
    template_name = 'boardgames/request_games.html'
    context_object_name = 'boardgames'
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get('name')
        name_type = self.request.GET.get('name_type', 'all')
        queryset = []

        if name:
            queryset = BGGSearch.fetch_items(name, name_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', '')
        context['name_type'] = self.request.GET.get('name_type', 'all')

        # get page objects and their bgg_id
        page_objects = context['object_list']
        bgg_ids = [game['bgg_id'] for game in page_objects]

        # get requests assigned to each bgg_id (if any)
        # append request info to corresponding page objects
        game_requests = GameRequest.objects.filter(
            board_game__bgg_id__in=bgg_ids,
            status=GameRequest.Status.PENDING,
        )

        game_requests_bgg_ids = [game_request.board_game.bgg_id for game_request in game_requests]

        ic(game_requests)
        ic(game_requests_bgg_ids)

        for game in page_objects:
            if game['bgg_id'] in str(game_requests_bgg_ids):
                game['game_request'] = True
                continue
            game['game_request'] = False
        ic(page_objects)

        return context


class RequestedBoardgamesView(LoginRequiredMixin, ListView):
    template_name = 'boardgames/requested_games.html'
    context_object_name = 'boardgames'
    model = BoardGame
    paginate_by = 10

    def get_queryset(self):
        queryset = BoardGame.objects.filter(
                status=BoardGame.Status.REQUESTED,
            )
        return queryset


class AcceptedBoardgamesView(LoginRequiredMixin, ListView):
    template_name = 'boardgames/accepted_games.html'
    context_object_name = 'boardgames'
    model = BoardGame
    paginate_by = 10

    def get_queryset(self):
        queryset = BoardGame.objects.filter(
                status=BoardGame.Status.ACCEPTED,
            )
        return queryset


class BoardgameDetailViewBGG(TemplateView):
    template_name = 'boardgames/details_bgg.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bgg_id = self.kwargs.get('bgg_id')

        if not bgg_id:
            return HttpResponseNotFound

        # check if boardgame is already in the db
        board_game = BoardGame.objects.filter(
            bgg_id=bgg_id,
            status=BoardGame.Status.REQUESTED
        )

        if board_game.exists():
            details = board_game.values().first()
            ic("Game fetched from DB")

            # check if boardgame has a pending request
            board_game_request = GameRequest.objects.filter(
                board_game=board_game.first(),
                status=GameRequest.Status.PENDING
            )

            if board_game_request.exists():
                # check how many users request the game and append request id
                users = board_game_request.first().users.all()
                context['request_exist'] = True
                context['users_amount'] = users.count()
                context['request_id'] = board_game_request.first().id

                if self.request.user in users:
                    # check if current user is requesting the game
                    context['user_sent_request'] = True

        else:
            details = BGGItemDetails.fetch_item(bgg_id)
            ic("Game fetched BGG API")

        context['form'] = GameRequestForm(initial=details)
        context['details'] = details
        context['bgg_detail_url'] = settings.BGG_GAME_DETAIL_URL
        return context


class BoardgameDetailView(DetailView):
    template_name = 'boardgames/details.html'
    model = BoardGame

    def get_queryset(self):
        # display only supported games!
        queryset = super().get_queryset()
        queryset = queryset.filter(status=BoardGame.Status.SUPPORTED)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bgg_detail_url'] = settings.BGG_GAME_DETAIL_URL
        return context


class RequestCreateUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        next_url = request.POST.get('next', 'boardgames:request_games')
        form = GameRequestForm(request.POST)

        if form.is_valid():
            ic(form.cleaned_data)

            bgg_id = form.cleaned_data['bgg_id']
            requesting_user = self.request.user

            game = BoardGame.objects.filter(bgg_id=bgg_id).first()

            if not game:
                # If game not in DB, add it
                ic('Creating new game object...')
                game = BoardGame.objects.create(
                    status=BoardGame.Status.REQUESTED,
                    bgg_id=bgg_id,
                    primary_name=form.cleaned_data['primary_name'],
                    description=form.cleaned_data['description'],
                    release_year=parse_date(form.cleaned_data['release_year']),
                    players_min=form.cleaned_data['players_min'],
                    players_max=form.cleaned_data['players_max'],
                    playtime_min=form.cleaned_data['playtime_min'],
                    playtime_max=form.cleaned_data['playtime_max'],
                    image_url=form.cleaned_data['image_url'],
                    thumbnail_url=form.cleaned_data['thumbnail_url'],
                )
            elif game.status == BoardGame.Status.SUPPORTED:
                # if game supported, gtfo
                ic('Game exists and is supported!')
                return HttpResponseRedirect(next_url)

            game_request = GameRequest.objects.filter(
                status=GameRequest.Status.PENDING,
                board_game=game,
            ).first()

            if not game_request:
                # for cases where previous requests were rejected (game in db but no request)
                ic('Creating request...')
                game_request = GameRequest.objects.create(
                    status=GameRequest.Status.PENDING,
                    board_game=game,
                )

            ic(requesting_user, game_request.users.all())
            if requesting_user not in game_request.users.all():
                ic('Adding user to request...')
                game_request.users.add(requesting_user, through_defaults={})
        else:
            print(form.errors)

        return HttpResponseRedirect(next_url)


class RequestCancelView(LoginRequiredMixin, View):
    def post(self, request):
        next_url = request.POST.get('next', 'boardgames:request_games')
        request_id = request.POST.get('request_id', None)
        requesting_user = self.request.user

        game_request = get_object_or_404(GameRequest, id=request_id)

        request_users = game_request.users.all()
        request_users_amount = request_users.count()

        if requesting_user in request_users:
            game_request.users.remove(requesting_user)
            request_users_amount -= 1

        if request_users_amount == 0:
            game_request.cancel()

        return HttpResponseRedirect(next_url)


class RequestAcceptView(LoginRequiredMixin, View):
    def post(self, request):
        form = RequestAcceptForm(request.POST)
        redirect_url = 'boardgames:accepted_games'

        if form.is_valid():
            game_id = form.cleaned_data['game_id']
            request_id = form.cleaned_data['request_id']

            game_request = get_object_or_404(GameRequest, id=request_id)
            if not game_request.accept():
                ic('Integrity error, request not accepted!')

            redirect_url = reverse('boardgames:update', kwargs={'pk': game_id})

        return HttpResponseRedirect(redirect_url)


class UpdateBoardGameView(LoginRequiredMixin, UpdateView):
    model = BoardGame
    template_name = 'boardgames/update.html'
    fields = [
        'primary_name',
        'description',
        'description_short',
        'release_year',
        'players_min',
        'players_max',
        'playtime_min',
        'playtime_max',
        'image_url',
        'thumbnail_url',
    ]

    def get_queryset(self):
        # only accepted games allowed!
        queryset = super().get_queryset()
        queryset = queryset.filter(status=BoardGame.Status.ACCEPTED)
        return queryset
