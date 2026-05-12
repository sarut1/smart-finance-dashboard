from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.goal_list, name='list'),
    path('create/', views.goal_create, name='create'),
    path('deposit/<int:pk>/', views.goal_deposit, name='deposit'),
    path('delete/<int:pk>/', views.goal_delete, name='delete'),
]