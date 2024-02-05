from django.urls import path, include

from .views import (
    BrowseGamesView,
    RequestGamesView,
    RequestedGamesView,
    AcceptedGamesView,
    GameDetailView,
    GameDetailViewBGG,
    CreateRequestExistingGameView,
    CreateRequestNewGameView,
    UpdateRequestView,
    CancelRequestView,
    AcceptRequestView,
    UpdateGameView,
    GameCollectionView,
    GameCollectionAddView,
    GameCollectionRemoveView,
)


NAMESPACE = 'games'
URL_PREFIX = 'games/'


patterns = [
    path('browse/', BrowseGamesView.as_view(), name='browse_games'),
    path('request/', RequestGamesView.as_view(), name='request_games'),
    path('<int:pk>/', GameDetailView.as_view(), name='details'),
    path('bgg-item/<int:bgg_id>/', GameDetailViewBGG.as_view(), name='details_bgg'),
    path('request/create/new-game', CreateRequestNewGameView.as_view(), name='request_create_new'),
    path('request/create/existing-game', CreateRequestExistingGameView.as_view(), name='request_create_existing'),
    path('request/cancel/', CancelRequestView.as_view(), name='request_cancel'),
    path('request/update/', UpdateRequestView.as_view(), name='request_update'),
    path('request/accept/', AcceptRequestView.as_view(), name='request_accept'),
    path('manage/requested/', RequestedGamesView.as_view(), name='requested_games'),
    path('manage/accepted/', AcceptedGamesView.as_view(), name='accepted_games'),
    path('manage/update/<int:pk>/', UpdateGameView.as_view(), name='update'),
    path('collection/<int:user_id>/', GameCollectionView.as_view(), name='collection'),
    path('collection/add/', GameCollectionAddView.as_view(), name='collection_add'),
    path('collection/remove/', GameCollectionRemoveView.as_view(), name='collection_remove'),
]

namespace_patterns = (patterns, NAMESPACE)

urlpatterns = [
    path(f'{URL_PREFIX}', include(namespace_patterns)),
]