from django.urls import path
from . import views

app_name='product'


urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='single'),
    path('add/', views.add, name='add'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('category/', views.category, name='category'),
    path('addcategory/', views.add_category, name='add_category'),
    path('editcategory/<int:id>/', views.edit_category, name='edit_category'),
    path('deleteproduct/<int:id>/', views.delete_product, name='delete_product'),
    path('deletecategory/<int:id>/', views.delete_category, name='delete_category'),


    path('request/', views.product_request, name='product_request'),
    path('request/<int:id>/', views.product_request_detail, name='product_request_detail'),
    path('update/<int:id>/', views.update, name='update'),
    path('product_request_delete/<int:id>/', views.product_request_delete, name='product_request_delete'),

]