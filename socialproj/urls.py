from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views  # import home view from accounts app
from django.conf import settings
from django.conf.urls.static import static

app_name = 'posts'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home_view, name='home'),  # root URL
    path('accounts/', include('accounts.urls')),      # login/logout URLs in accounts/urls.py
    path('posts/', include('posts.urls')), 
               path('', include('posts.urls', namespace='posts')),
           # your posts app URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
