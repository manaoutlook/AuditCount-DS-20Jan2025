from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('roles/', views.manage_roles, name='manage_roles'),
    path('roles/delete/<int:id>/', views.delete_role, name='delete_role'),
    path('permissions/', views.manage_permissions, name='manage_permissions'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:id>/update/', views.update_user, name='update_user'),
    path('users/<int:id>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:id>/', views.get_user, name='get_user'),
    path('access-denied/', views.access_denied, name='access_denied'),
    
    # Location-related URLs
    path('locations/', views.manage_locations, name='manage_locations'),
    path('locations/create/', views.create_location, name='create_location'),
    path('locations/<int:id>/update/', views.update_location, name='update_location'),
    path('locations/<int:id>/delete/', views.delete_location, name='delete_location'),
    path('locations/<int:id>/', views.get_location, name='get_location'),
]
