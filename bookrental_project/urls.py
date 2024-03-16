from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('auth-admin/', admin.site.urls),
    path('', include(('apps.users.urls', 'users'))),
    path('', include(('apps.core.urls', 'core'))),
    # path('', include('pages.urls', namespace='pages')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
