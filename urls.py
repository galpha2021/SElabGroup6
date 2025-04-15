from django.urls import path
from .views import DeleteAccountView
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from .views import seller_dashboard
from .views import admin_monitor_products

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('delete/', DeleteAccountView.as_view(), name='delete_account'),
    path('', views.homepage_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('loggedout/', views.loggedout_view, name='loggedout'),

    
    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
    path('admin/users/', admin_monitor_users, name='admin_users'),
    path('admin/products/', admin_monitor_products, name='admin_products'),
]
