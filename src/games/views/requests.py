from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View

from ..models import Game, GameRequest
from ..forms import GameRequestForm, RequestAcceptForm

from icecream import ic


class CreateRequestView(LoginRequiredMixin, View):
    def create_new_game_request(self, game) -> GameRequest:
        game_request = GameRequest.objects.create(
            status=GameRequest.Status.PENDING,
            game=game,
        )
        return game_request


class CreateRequestExistingGameView(CreateRequestView):
    ALLOWED_STATUSES = (
        Game.Status.REJECTED,
        Game.Status.DORMANT,
    )

    def post(self, request):
        requesting_user = self.request.user
        next_url_default = 'games:request_games'

        next_url = request.POST.get('next', next_url_default)
        game_id = request.POST.get('game_id')

        game = get_object_or_404(Game, id=game_id)

        if game.status not in self.ALLOWED_STATUSES:
            # this is done to prevent creating new requests when game is supported or in review
            ic('Game exists and its status except it from creating new request')
            return HttpResponseRedirect(next_url_default)

        game_request = GameRequest.objects.filter(
            status=GameRequest.Status.PENDING,
            game=game,
        )

        if game_request.exists():
            ic('Pending game request already exists!')
            return HttpResponseRedirect(next_url_default)

        ic('Creating request...')
        try:
            with transaction.atomic():
                game_request = self.create_new_game_request(game)
                game_request.users.add(requesting_user, through_defaults={})
                game.status = Game.Status.REQUESTED
                game.save()
        except IntegrityError:
            ic('Failed while creating request')
        return HttpResponseRedirect(next_url)


class CreateRequestNewGameView(CreateRequestView):

    def create_new_game(self, form) -> Game:
        game = Game.objects.create(
            status=Game.Status.REQUESTED,
            bgg_id=form.cleaned_data['bgg_id'],
            primary_name=form.cleaned_data['primary_name'],
            description=form.cleaned_data['description'],
            release_year=form.cleaned_data['release_year'],
            players_min=form.cleaned_data['players_min'],
            players_max=form.cleaned_data['players_max'],
            playtime_min=form.cleaned_data['playtime_min'],
            playtime_max=form.cleaned_data['playtime_max'],
            image_url=form.cleaned_data['image_url'],
            thumbnail_url=form.cleaned_data['thumbnail_url'],
        )
        return game

    def post(self, request):
        requesting_user = self.request.user
        next_url_default = 'games:request_games'

        next_url = request.POST.get('next', next_url_default)
        form = GameRequestForm(request.POST)

        if form.is_valid():

            game = Game.objects.filter(bgg_id=form.cleaned_data['bgg_id'])

            if game.exists():
                ic('Game already exists! Wrong endpoint')
                return HttpResponseRedirect(next_url_default)

            ic('Creating new game object...')
            game = self.create_new_game(form)
            next_url = reverse('games:details', kwargs={'pk': game.id})

            ic('Creating request...')

            try:
                with transaction.atomic():
                    game_request = self.create_new_game_request(game)
                    game_request.users.add(requesting_user, through_defaults={})
            except IntegrityError:
                ic('Failed while creating request')
        else:
            ic(form.errors)

        return HttpResponseRedirect(next_url)


class UpdateRequestView(LoginRequiredMixin, View):
    def post(self, request):
        requesting_user = self.request.user
        next_url_default = 'games:request_games'

        next_url = request.POST.get('next', next_url_default)
        request_id = request.POST.get('request_id')

        game_request = get_object_or_404(
            GameRequest,
            id=request_id,
            status=GameRequest.Status.PENDING,
        )

        ic(requesting_user, game_request.users.all())
        if requesting_user not in game_request.users.all():
            ic('Adding user to request...')
            game_request.users.add(requesting_user, through_defaults={})
        else:
            ic('User is already requesting the game!')

        return HttpResponseRedirect(next_url)


class CancelRequestView(LoginRequiredMixin, View):
    def post(self, request):
        next_url = request.POST.get('next', 'games:request_games')
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


class AcceptRequestView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'games.accept_game_request'

    def post(self, request):
        form = RequestAcceptForm(request.POST)
        redirect_url = 'games:accepted_games'

        if form.is_valid():
            game_id = form.cleaned_data['game_id']
            request_id = form.cleaned_data['request_id']

            game_request = get_object_or_404(GameRequest, id=request_id)
            if not game_request.accept():
                ic('Integrity error, request not accepted!')
            else:
                redirect_url = reverse('games:update', kwargs={'pk': game_id})

        return HttpResponseRedirect(redirect_url)
