from django.urls import path, reverse_lazy
from . import views

app_name='account'


urlpatterns = [
    path('', views.admin_users, name='admin_users'),
    path('create_admin/', views.create_admin, name='create_admin'),
    path('users', views.users, name='users'),
    path('create_user/', views.create_user, name='create_user'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
]