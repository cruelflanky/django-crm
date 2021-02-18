from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.dashboard, name = 'index'),
	path('signup/', views.signup, name = 'signup'),
	path('profile/', views.profile, name = 'profile'),
	path('profile/edit/', views.profile_edit, name = 'edit'),
	path('orders/', views.orders, name = 'orders'),
	path('staff/', views.staff, name = 'staff'),
	path('delete_profile/<str:pk>/', views.delete_profile, name="delete_profile"),
	path('update_profile/<str:pk>/', views.update_profile, name="update_profile"),
	path('set_payment/<str:pk>/', views.set_payment, name="set_payment"),
	path('teams/', views.teams, name = 'teams'),
	path('delete_team/<str:pk>/', views.delete_team, name="delete_team"),
	path('no_permision/', views.no_permision, name = 'no_permision'),
	path('my_clients/', views.my_clients, name = 'my_clients'),
	path('my_clients/all_clients', views.all_clients, name = 'all_clients'),
	path('delete_shop/<str:pk>/', views.delete_shop, name="delete_shop"),
	path('update_shop/<str:pk>/', views.update_shop, name="update_shop"),
	path('bd_search/', views.bd_search, name = 'bd_search'),
	path('dublicates/', views.dublicates, name = 'dublicates'),
	path('relink_shops/', views.relink_shops, name = 'relink_shops'),
]
