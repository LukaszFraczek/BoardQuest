from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView


from .models import BoardGame
from .utils import BGGSearch, BGGItemDetails

from icecream import ic


class BoardgameSearchView(LoginRequiredMixin, ListView):
    template_name = 'boardgames/search.html'
    context_object_name = 'boardgames'
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get('name')
        name_type = self.request.GET.get('name_type')

        if name:
            queryset = BGGSearch.fetch_items(name.lower(), name_type)
            return queryset
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', '')
        context['name_type'] = self.request.GET.get('name_type', 'all')
        return context


class BoardgameBGGDetailView(TemplateView):
    template_name = 'boardgames/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bgg_id = self.kwargs.get('bgg_id')

        if bgg_id:
            details = BGGItemDetails.fetch_item(bgg_id)
            context['details'] = details

        return context
