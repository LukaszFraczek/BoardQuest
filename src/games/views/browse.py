from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import Game
from ..bgg_api import BGGSearch

from typing import Dict, List
from icecream import ic


class BrowseGamesView(LoginRequiredMixin, ListView):
    template_name = 'games/list/browse_games.html'
    context_object_name = 'games'
    model = Game
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get('name')
        queryset = Game.objects.filter(
                status=Game.Status.SUPPORTED,
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


class RequestGamesView(LoginRequiredMixin, ListView):
    template_name = 'games/list/request_games.html'
    context_object_name = 'games'
    paginate_by = 10

    def get_games_details(self, games: List[Dict]) -> Dict:
        """Get game status and id of each game in the list"""

        games_bgg_ids = [game['bgg_id'] for game in games]

        games_in_db = Game.objects.filter(bgg_id__in=games_bgg_ids)

        if games_in_db.exists():
            games_details = dict()
            for game in games_in_db:
                details = {
                    'id': game.id,
                    'status': game.status,
                }
                games_details.update({game.bgg_id: details})

            return games_details
        return {}

    def update_games_details(self, games: List[Dict]) -> None:
        """In-place update of game dicts contained in provided list"""

        details = self.get_games_details(games)
        no_details = {
            'id': None,
            'status': None,
        }

        for game in games:
            bgg_id = int(game['bgg_id'])
            if bgg_id in details.keys():
                game_details = details[bgg_id]
                game.update(game_details)
            else:
                game.update(no_details)

    def get_queryset(self):
        name = self.request.GET.get('name')
        name_type = self.request.GET.get('name_type', 'all')
        queryset = []

        if name:
            queryset = BGGSearch.fetch_items(name, name_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get('name', '')
        name_type = self.request.GET.get('name_type', 'all')

        context['name'] = name
        context['name_type'] = name_type
        context['querystring'] = f'name={name}&name_type={name_type}&'

        page_games = context['object_list']
        if page_games:
            self.update_games_details(page_games)

        ic(context)

        return context
