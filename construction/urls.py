from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Main Application URLs
    path('', views.dashboard, name='dashboard'),
    path('stock/', views.view_stock, name='view_stock'),
    path('stock/edit/<int:stock_id>/', views.edit_stock, name='edit_stock'),
    path('arrival/', views.register_arrival, name='register_arrival'),
    path('usage/', views.register_usage, name='register_usage'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]