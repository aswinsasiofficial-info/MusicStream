from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('library/', views.library, name='library'),
    
    # API endpoints
    path('api/search/', views.search_api, name='search_api'),
    path('api/popular/', views.popular_api, name='popular_api'),
    path('api/track/<str:track_id>/', views.track_detail_api, name='track_detail_api'),
]
