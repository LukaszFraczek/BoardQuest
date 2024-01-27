from django.conf import settings
from django.http import HttpResponseNotFound
from django.views.generic import DetailView, TemplateView

from ..models import Game, GameRequest
from ..bgg_api import BGGItemDetails
from ..forms import GameRequestForm

from icecream import ic


class GameDetailViewBGG(TemplateView):
    template_name = 'games/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bgg_id = self.kwargs.get('bgg_id')

        if not bgg_id:
            return HttpResponseNotFound

        game_details = BGGItemDetails.fetch_item(bgg_id)

        context['form'] = GameRequestForm(initial=game_details)
        context['object'] = game_details
        context['bgg_detail_url'] = settings.BGG_GAME_DETAIL_URL
        return context


class GameDetailView(DetailView):
    template_name = 'games/details.html'
    model = Game

    def get_game_request_data(self, game_obj) -> dict:
        """Returns context data for game request"""

        data = dict()

        game_request = GameRequest.objects.filter(
            game=game_obj,
            status=GameRequest.Status.PENDING,
        )

        if game_request.exists():
            users = game_request.first().users.all()
            data['request_id'] = game_request.first().id
            data['user_sent_request'] = True if self.request.user in users else False
            data['users_amount'] = users.count()

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.status == Game.Status.REQUESTED:
            game_request_data = self.get_game_request_data(self.object)
            context.update(game_request_data)

        context['bgg_detail_url'] = settings.BGG_GAME_DETAIL_URL
        return context
