from django.conf import settings
from django.http import HttpResponseNotFound
from django.views.generic import DetailView, TemplateView

from ..models import Game, GameRequest
from ..bgg_api import BGGItemDetails
from ..forms import GameRequestForm

from icecream import ic


class GameDetailViewBGG(TemplateView):
    template_name = 'games/details_bgg.html'

    def get_game_request_data(self, game_obj) -> dict:
        """Returns context data for game request"""

        data = dict()

        game_request = GameRequest.objects.filter(
            game=game_obj,
            status=GameRequest.Status.PENDING,
        )

        if game_request.exists():
            users = game_request.first().users.all()
            data['user_sent_request'] = True if self.request.user in users else False
            data['request_exist'] = True
            data['users_amount'] = users.count()
            data['request_id'] = game_request.first().id
        else:
            data['request_exist'] = False

        return data

    def get_game_values(self, bgg_id) -> (dict, dict):
        context = dict()
        game = Game.objects.filter(bgg_id=bgg_id)

        if game.exists():
            ic("Game fetched from DB")
            game_obj = game.first()
            game_details = game.values().first()

            game_request_data = self.get_game_request_data(game_obj)
            context.update(game_request_data)
        else:
            ic("Game fetched BGG API")
            game_details = BGGItemDetails.fetch_item(bgg_id)

        return context, game_details

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bgg_id = self.kwargs.get('bgg_id')

        if not bgg_id:
            return HttpResponseNotFound

        game_context, game_details = self.get_game_values(bgg_id)

        context.update(game_context)
        context['form'] = GameRequestForm(initial=game_details)
        context['details'] = game_details
        context['bgg_detail_url'] = settings.BGG_GAME_DETAIL_URL
        return context


class GameDetailView(DetailView):
    template_name = 'games/details.html'
    model = Game

    def get_queryset(self):
        # display only supported games!
        queryset = super().get_queryset()
        queryset = queryset.filter(status=Game.Status.SUPPORTED)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bgg_detail_url'] = settings.BGG_GAME_DETAIL_URL
        return context
