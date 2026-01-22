from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    path('', include('accounts.urls')),
    path('', include('posts.urls')),
]

# 🔥 THIS PART IS REQUIRED FOR IMAGES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
