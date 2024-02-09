from django.conf import settings
from django.contrib.auth.models import Group
from django.core.cache import cache


def groups_processor(request):
    groups = cache.get('all_groups')
    if not groups:
        groups = {group.name.lower(): group for group in Group.objects.all()}
        cache.set('all_groups', groups, timeout=settings.GROUP_CACHE_PERSISTENCE)
    return {'groups': groups}


def user_groups_processor(request):
    user_groups = []
    user = request.user
    if user.is_authenticated:
        user_groups = list(user.groups.values_list('name', flat=True))
    return {'user_groups': user_groups}
