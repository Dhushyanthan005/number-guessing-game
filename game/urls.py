from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new-game/', views.new_game, name='new_game'),
    path('game/<int:game_id>/', views.guess_view, name='guess'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]