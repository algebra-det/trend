from django.urls import path
from . import views

app_name='game'


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.single, name='single'),
    path('creategame/', views.create_game, name='create_game'),
    path('editgame/<int:id>/', views.edit_game, name='edit_game'),
    path('deletegame/<int:id>/', views.delete_game, name='delete_game'),

    path('<int:id>/challenge/', views.challenge, name='challenge'),
    path('singlechallenge/<int:id>/', views.single_challenge, name='single_challenge'),
    path('<int:id>/createchallenge/', views.create_challenge, name='create_challenge'),
    path('editchallenge/<int:id>/', views.edit_challenge, name='edit_challenge'),
    path('deletechallenge/<int:id>/', views.delete_challenge, name='delete_challenge'),

    path('promotion/create/<int:id>/', views.create_promotion, name='create_promotion'),
    path('promotion/edit/<int:id>/', views.edit_promotion, name='edit_promotion'),
    path('promotion/delete/<int:id>/', views.delete_promotion, name='delete_promotion')
]