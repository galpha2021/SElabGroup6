from django.urls import path
from django.urls import path, include

#from .views import DeleteAccountView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('delete/', views.delete_account_view, name='delete_account'),
    path('', views.homepage_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('loggedout/', views.loggedout_view, name='loggedout'),
    path('seller/', views.seller_dashboard, name='seller'),
    path('update/', views.update_view, name='update'),
    path('', views.update_updatedb, name='update_updatedb'),
    path('seller/add/', views.add_item, name='seller_add'),
    path('seller/update-or-delete/', views.seller_update_or_delete, name='seller_update_or_delete'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('transactions/', views.view_transactions, name='transactions'),
    path('admin/monitor/users/', views.admin_monitor_users, name='admin_monitor_users'),
    path('admin/monitor/products/', views.admin_monitor_products, name='admin_monitor_products'),
    path('admin/delete_account/<int:user_id>/', views.admin_delete_account, name='admin_delete_account'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('homepage/', views.search_items, name='search_items'),

]

