from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.FeedView.as_view(), name='feed'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    
    
]
