from django.urls import path
from . import views

app_name='core'


urlpatterns = [
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('', views.index, name='index'),
    path('reward/', views.reward, name='reward'),
    path('settings/', views.settings, name='settings'),
    path('privacy/', views.privacy_edit, name='privacy'),
    path('conditions/', views.conditions_edit, name='conditions'),
    path('credits/', views.credits_edit, name='credits'),
]