from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import Game
from ..bgg_api import BGGSearch

from typing import Dict, Any
from icecream import ic


class BrowseGamesView(LoginRequiredMixin, ListView):
    template_name = 'games/browse_games.html'
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
    template_name = 'games/request_games.html'
    context_object_name = 'games'
    paginate_by = 10

    def add_games_status(self, context: Dict[str, Any]) -> None:
        """Get game status and add it to each game in the context"""

        page_games = context['object_list']

        if not page_games:
            return

        page_games_bgg_ids = [game['bgg_id'] for game in page_games]

        db_games = Game.objects.filter(bgg_id__in=page_games_bgg_ids)

        if db_games.exists():
            db_games_statuses = {game.bgg_id: game.status for game in db_games}
            db_games_bgg_ids = db_games_statuses.keys()

            for page_game in page_games:
                page_game_bgg_id = int(page_game['bgg_id'])
                if page_game_bgg_id in db_games_bgg_ids:
                    status = {'status': db_games_statuses[page_game_bgg_id]}
                else:
                    status = {'status': None}
                # this works because page_games is reference to a list in the context
                page_game.update(status)
        else:
            for page_game in page_games:
                page_game.update({'status': None})

        ic(page_games)

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

        self.add_games_status(context)

        return context
