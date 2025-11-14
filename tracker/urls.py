from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('shows/', views.show_list, name='show_list'),
    path('shows/add/', views.add_show, name='add_show'),
    path('shows/<int:pk>/', views.show_detail, name='show_detail'),
]
