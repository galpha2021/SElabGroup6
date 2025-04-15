from django.urls import path
from .views import DeleteAccountView
from . import views
from .views import seller_dashboard

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('delete/', DeleteAccountView.as_view(), name='delete_account'),
    path('', views.homepage_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('loggedout/', views.loggedout_view, name='loggedout'),

    
    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
]
