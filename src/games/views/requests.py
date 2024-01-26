from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.views.generic import View

from ..models import Game, GameRequest
from ..forms import GameRequestForm, RequestAcceptForm

from icecream import ic


class RequestCreateUpdateView(LoginRequiredMixin, View):
    ALLOWED_STATUSES = (
        Game.Status.REQUESTED,
        Game.Status.REJECTED,
    )

    def create_new_game(self, form) -> Game:
        game = Game.objects.create(
            status=Game.Status.REQUESTED,
            bgg_id=form.cleaned_data['bgg_id'],
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
        return game

    def create_new_game_request(self, game) -> GameRequest:
        game_request = GameRequest.objects.create(
            status=GameRequest.Status.PENDING,
            game=game,
        )
        return game_request

    def post(self, request):
        next_url = request.POST.get('next', 'games:request_games')
        form = GameRequestForm(request.POST)

        if form.is_valid():
            requesting_user = self.request.user

            game = Game.objects.filter(
                bgg_id=form.cleaned_data['bgg_id']
            ).first()

            if not game:
                ic('Creating new game object...')
                game = self.create_new_game(form)

            elif game.status not in self.ALLOWED_STATUSES:
                # this is done to prevent creating new requests when game is supported or in review
                ic('Game exists and its status except it from proceeding')
                return HttpResponseRedirect(next_url)

            game_request = GameRequest.objects.filter(
                status=GameRequest.Status.PENDING,
                game=game,
            ).first()

            if not game_request:
                # for cases where previous requests were rejected (game in db but no request)
                ic('Creating request...')
                game_request = self.create_new_game_request(game)

            ic(requesting_user, game_request.users.all())
            if requesting_user not in game_request.users.all():
                ic('Adding user to request...')
                game_request.users.add(requesting_user, through_defaults={})
        else:
            ic(form.errors)

        return HttpResponseRedirect(next_url)


class RequestCancelView(LoginRequiredMixin, View):
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


class RequestAcceptView(LoginRequiredMixin, View):
    def post(self, request):
        form = RequestAcceptForm(request.POST)
        redirect_url = 'games:accepted_games'

        if form.is_valid():
            game_id = form.cleaned_data['game_id']
            request_id = form.cleaned_data['request_id']

            game_request = get_object_or_404(GameRequest, id=request_id)
            if not game_request.accept():
                ic('Integrity error, request not accepted!')

            redirect_url = reverse('games:update', kwargs={'pk': game_id})

        return HttpResponseRedirect(redirect_url)
