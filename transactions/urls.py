from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.transaction_list, name='list'),
    path('create/', views.transaction_create, name='create'),
    path('edit/<int:pk>/', views.transaction_edit, name='edit'),
    path('delete/<int:pk>/', views.transaction_delete, name='delete'),
    path('category/create/', views.category_create, name='category_create'),
]