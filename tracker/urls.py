from django.urls import path
from tracker import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    path('register/', views.register, name='register'),
    path("login/", views.custom_login, name="login"),
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_edit_expense, name='add_expense'),
    path('edit/<int:pk>/', views.add_edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('logout/',views.custom_logout, name='logout'),
    path("filter_expenses/", views.filter_expenses, name="filter_expenses"),
]
