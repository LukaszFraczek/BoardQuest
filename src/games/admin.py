from django.contrib import admin
from .models import (
    Game,
    GameList,
    GameListEntry,
    GameRequest,
    GameRequestUser,
)


admin.site.register(Game)
admin.site.register(GameList)
admin.site.register(GameListEntry)
admin.site.register(GameRequest)
admin.site.register(GameRequestUser)
