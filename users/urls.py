from django.urls import path
from django.urls import path, include
#from .views import DeleteAccountView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    #path('delete/', DeleteAccountView.as_view(), name='delete_account'),
    path('delete/', views.delete_account_view, name='delete_account'),
    path('', views.homepage_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('loggedout/', views.loggedout_view, name='loggedout'),
    #path('seller/', views.seller_view, name='seller'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('update/', views.update_view, name='update'),
    path('', views.update_updatedb, name='update_updatedb')

]
