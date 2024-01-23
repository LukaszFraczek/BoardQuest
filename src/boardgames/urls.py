from django.urls import path, include

from .views import (
    BrowseBoardgamesView,
    RequestBoardgamesView,
    RequestedBoardgamesView,
    BoardgameDetailView,
    BoardgameDetailViewBGG,
    RequestCreateView,
    RequestCancelView,
)


NAMESPACE = 'boardgames'
URL_PREFIX = 'boardgames/'


patterns = [
    path('browse-games/', BrowseBoardgamesView.as_view(), name='browse_games'),
    path('request-games/', RequestBoardgamesView.as_view(), name='request_games'),
    path('requested-games/', RequestedBoardgamesView.as_view(), name='requested_games'),
    path('<int:pk>/', BoardgameDetailView.as_view(), name='details'),
    path('bgg-item/<int:bgg_id>/', BoardgameDetailViewBGG.as_view(), name='details_bgg'),
    path('request/create/', RequestCreateView.as_view(), name='request_create'),
    path('request/cancel/', RequestCancelView.as_view(), name='request_cancel'),
]

namespace_patterns = (patterns, NAMESPACE)

urlpatterns = [
    path(f'{URL_PREFIX}', include(namespace_patterns)),
]