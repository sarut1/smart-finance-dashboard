from django.urls import path
from . import views

app_name = 'budgets'

urlpatterns = [
    path('', views.budget_list, name='list'),
    path('create/', views.budget_create, name='create'),
    path('delete/<int:pk>/', views.budget_delete, name='delete'),
]