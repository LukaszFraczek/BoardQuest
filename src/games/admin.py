from django.contrib import admin
from .models import (
    Game,
    GameCollection,
    GameCollectionEntry,
    GameRequest,
    GameRequestUser,
)


admin.site.register(Game)
admin.site.register(GameCollection)
admin.site.register(GameCollectionEntry)
admin.site.register(GameRequest)
admin.site.register(GameRequestUser)
