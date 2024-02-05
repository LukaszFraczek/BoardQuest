from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, View
from django.http import HttpResponseRedirect

from ..models import Game, GameCollection


class GameCollectionView(LoginRequiredMixin, ListView):
    template_name = 'games/list/browse_collection.html'
    context_object_name = 'games'
    model = Game
    paginate_by = 10

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        game_collection = get_object_or_404(GameCollection, user=user_id)
        queryset = game_collection.games.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        context['collection_user'] = get_object_or_404(User, id=user_id)
        return context


class GameCollectionAddView(LoginRequiredMixin, View):
    def post(self, request):
        current_user = self.request.user

        game_id = request.POST.get('game_id')

        game = get_object_or_404(
            Game,
            id=game_id,
            status=Game.Status.SUPPORTED,
        )

        current_user.collection.add(game)

        game_details_url = reverse('games:details', kwargs={'pk': game_id})
        next_url = request.POST.get('next', game_details_url)

        return HttpResponseRedirect(next_url)


class GameCollectionRemoveView(LoginRequiredMixin, View):
    def post(self, request):
        current_user = self.request.user

        game_id = request.POST.get('game_id')

        game = get_object_or_404(
            Game,
            id=game_id,
            status=Game.Status.SUPPORTED,
        )

        current_user.collection.remove(game)

        game_details_url = reverse('games:details', kwargs={'pk': game_id})
        next_url = request.POST.get('next', game_details_url)

        return HttpResponseRedirect(next_url)
