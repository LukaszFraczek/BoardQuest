from django.urls import path, include

NAMESPACE = 'boardgames'
URL_PREFIX = 'boardgames/'


patterns = [
]

namespace_patterns = (patterns, NAMESPACE)

urlpatterns = [
    path('', include(namespace_patterns)),
]
