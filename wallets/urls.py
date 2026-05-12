from django.urls import path
from . import views

app_name = 'wallets'

urlpatterns = [
    path('', views.wallet_list, name='list'),
    path('create/', views.wallet_create, name='create'),
    path('delete/<int:pk>/', views.wallet_delete, name='delete'),
]