from django.urls import path, include

from .views import (
    BoardgameSearchView,
    BoardgameBGGDetailView,
)


NAMESPACE = 'boardgames'
URL_PREFIX = 'boardgames/'


patterns = [
    path('search/', BoardgameSearchView.as_view(), name='search'),
    path('<int:bgg_id>/', BoardgameBGGDetailView.as_view(), name='details_bgg'),
]

namespace_patterns = (patterns, NAMESPACE)

urlpatterns = [
    path(f'{URL_PREFIX}', include(namespace_patterns)),
]