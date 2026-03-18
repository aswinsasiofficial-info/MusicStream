from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('library/', views.library, name='library'),
    path('api/search/', views.search_api, name='search_api'),
    path('api/trending/', views.trending_api, name='trending_api'),
    path('api/home-content/', views.home_content_api, name='home_content_api'),
    path('api/song/<str:song_id>/', views.song_detail_api, name='song_detail_api'),
]
