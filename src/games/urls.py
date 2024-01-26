from django.urls import path, include

from .views import (
    BrowseGamesView,
    RequestGamesView,
    RequestedGamesView,
    AcceptedGamesView,
    GameDetailView,
    GameDetailViewBGG,
    RequestCreateUpdateView,
    RequestCancelView,
    RequestAcceptView,
    UpdateGameView,
)


NAMESPACE = 'games'
URL_PREFIX = 'games/'


patterns = [
    path('browse-games/', BrowseGamesView.as_view(), name='browse_games'),
    path('request-games/', RequestGamesView.as_view(), name='request_games'),
    path('requested-games/', RequestedGamesView.as_view(), name='requested_games'),
    path('accepted-games/', AcceptedGamesView.as_view(), name='accepted_games'),
    path('<int:pk>/', GameDetailView.as_view(), name='details'),
    path('bgg-item/<int:bgg_id>/', GameDetailViewBGG.as_view(), name='details_bgg'),
    path('request/create/', RequestCreateUpdateView.as_view(), name='request_create'),
    path('request/cancel/', RequestCancelView.as_view(), name='request_cancel'),
    path('request/accept/', RequestAcceptView.as_view(), name='request_accept'),
    path('update/<int:pk>/', UpdateGameView.as_view(), name='update'),
]

namespace_patterns = (patterns, NAMESPACE)

urlpatterns = [
    path(f'{URL_PREFIX}', include(namespace_patterns)),
]