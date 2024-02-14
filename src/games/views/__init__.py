from .browse import (
    SupportedGamesView,
    UnsupportedGamesView,
)
from .details import (
    GameDetailViewBGG,
    GameDetailView,
)
from .management import (
    RequestedGamesView,
    AcceptedGamesView,
    UpdateGameView,
)
from .requests import (
    CreateRequestExistingGameView,
    CreateRequestNewGameView,
    UpdateRequestView,
    CancelRequestView,
    AcceptRequestView,
)
from .collection import (
    GameCollectionView,
    GameCollectionAddView,
    GameCollectionRemoveView,
)


__all__ = [
    'SupportedGamesView',
    'UnsupportedGamesView',
    'RequestedGamesView',
    'AcceptedGamesView',
    'GameDetailView',
    'GameDetailViewBGG',
    'CreateRequestExistingGameView',
    'CreateRequestNewGameView',
    'UpdateRequestView',
    'CancelRequestView',
    'AcceptRequestView',
    'UpdateGameView',
    'GameCollectionView',
    'GameCollectionAddView',
    'GameCollectionRemoveView',
]