from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('posts.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('group/', include('posts.urls', namespace='group')),
    path('about/', include('about.urls', namespace='about')),
    path('administrator/', admin.site.urls),
]
