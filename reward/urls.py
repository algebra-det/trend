from django.urls import path
from . import views

app_name = 'reward'

urlpatterns = [
    path('trophies/', views.trophies, name="trophies"),
    path('trophies/detail/<int:id>/', views.trophy_detail, name="trophy_detail"),
    path('trophies/create/', views.create_trophy, name="create_trophy"),
    path('trophies/update/<int:id>/', views.update_trophy, name="update_trophy"),
    path('trophies/delete/<int:id>/', views.delete_trophy, name="delete_trophy"),
    path('magic_box/', views.magic_boxes, name="magic_boxes"),
    path('magic_box/<int:id>/', views.magic_box_detail, name="magic_box_detail"),
    path('magic_box/create/', views.create_magic_boxes, name="create_magic_box"),
    path('magic_box/update/<int:id>/', views.update_magic_boxes, name="update_magic_box"),
    path('magic_box/delete/<int:id>/', views.delete_magic_boxes, name="delete_magic_box"),
]