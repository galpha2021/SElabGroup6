from django.urls import path
from .views import DeleteAccountView
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('delete/', DeleteAccountView.as_view(), name='delete_account'),
    path('homepage/', views.homepage_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('loggedout/', views.loggedout_view, name='loggedout'),
    path('seller/', views.seller_view, name='seller'),
]
