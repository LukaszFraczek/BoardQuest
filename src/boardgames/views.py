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
            queryset = BGGSearch.fetch_items(name.lower())
            return queryset
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', '')
        return context


class BoardgameBGGDetailView(DetailView):
    template_name = 'boardgames/details.html'


