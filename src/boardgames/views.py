from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

from .models import BoardGame
from .utils import BGGSearch

from icecream import ic


class BoardgameSearchView(LoginRequiredMixin, ListView):
    template_name = 'boardgames/search.html'
    context_object_name = 'boardgames'
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get('name')
        if name:
            games_list = BGGSearch.fetch_items(name)

            # Extract game IDs
            # game_ids = [game.get('id') for game in games_list]

            # ic(game_ids)

            # Use IDs to make a second API call for thumbnails
            # thumbnails = BGGSearch.fetch_thumbnails(game_ids)

            # Combine game information with their thumbnails.
            queryset = []
            for game in games_list:
                game_id = game.get('id')
                game_name = game.get('name')
                # thumbnail_url = [item['thumbnail'] for item in thumbnails if item['id'] == game_id],

                queryset.append(
                    {
                        'id': game_id,
                        'name': game_name,
                        # 'thumbnail': thumbnail_url,
                    }
                )

            return queryset
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', '')
        return context


class BoardgameBGGDetailView(DetailView):
    template_name = 'boardgames/details.html'


