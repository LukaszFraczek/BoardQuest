from django.contrib import admin

from .models import FriendList, FriendInvitation


class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    # readonly_fields = ['user']  # uncomment later

    class Meta:
        model = FriendList


class FriendInvitationAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_field = ['sender__username', 'receiver__username']

    class Meta:
        model = FriendInvitation


admin.site.register(FriendList, FriendListAdmin)
admin.site.register(FriendInvitation, FriendInvitationAdmin)
