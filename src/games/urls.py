from django.urls import path, include

from .views import (
    BrowseBoardgamesView,
    RequestBoardgamesView,
    RequestedBoardgamesView,
    AcceptedBoardgamesView,
    BoardgameDetailView,
    BoardgameDetailViewBGG,
    RequestCreateUpdateView,
    RequestCancelView,
    RequestAcceptView,
    UpdateBoardGameView,
)


NAMESPACE = 'games'
URL_PREFIX = 'games/'


patterns = [
    path('browse-games/', BrowseBoardgamesView.as_view(), name='browse_games'),
    path('request-games/', RequestBoardgamesView.as_view(), name='request_games'),
    path('requested-games/', RequestedBoardgamesView.as_view(), name='requested_games'),
    path('accepted-games/', AcceptedBoardgamesView.as_view(), name='accepted_games'),
    path('<int:pk>/', BoardgameDetailView.as_view(), name='details'),
    path('bgg-item/<int:bgg_id>/', BoardgameDetailViewBGG.as_view(), name='details_bgg'),
    path('request/create/', RequestCreateUpdateView.as_view(), name='request_create'),
    path('request/cancel/', RequestCancelView.as_view(), name='request_cancel'),
    path('request/accept/', RequestAcceptView.as_view(), name='request_accept'),
    path('update/<int:pk>/', UpdateBoardGameView.as_view(), name='update'),
]

namespace_patterns = (patterns, NAMESPACE)

urlpatterns = [
    path(f'{URL_PREFIX}', include(namespace_patterns)),
]