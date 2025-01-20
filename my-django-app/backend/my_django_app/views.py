from django.http import HttpResponse, JsonResponse
from .tables import LocationTable
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.cache import cache
from .models import Role, Location, User, Permission
from .forms import UserForm, RoleForm, PermissionForm, LocationForm

def index(request):
    return render(request, 'index.html')

@login_required
def manage_locations(request):
    locations = Location.objects.all()
    return render(request, 'manage_locations.html', {'locations': locations})

@login_required
def create_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location created successfully')
            return redirect('manage_locations')
        messages.error(request, 'Error creating location')
        # Show form with errors instead of redirecting
        return render(request, 'manage_locations.html', {
            'locations': Location.objects.all(),
            'form': form
        })
    # Handle GET requests
    return render(request, 'manage_locations.html', {
        'locations': Location.objects.all(),
        'form': LocationForm()
    })

@login_required
def update_location(request, id):
    location = get_object_or_404(Location, id=id)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location updated successfully')
            return redirect('manage_locations')
        messages.error(request, 'Error updating location')
    return redirect('manage_locations')

@login_required
def delete_location(request, id):
    try:
        with transaction.atomic():
            location = get_object_or_404(Location, id=id)
            if request.method == 'POST':
                location.delete()
                # Invalidate cache for locations
                cache.delete('all_locations')
                cache.delete(f'location_{id}')
                messages.success(request, 'Location deleted successfully')
                return redirect('manage_locations')
            messages.error(request, 'Invalid request method')
            return redirect('manage_locations')
    except Exception as e:
        messages.error(request, f'Error deleting location: {str(e)}')
        return redirect('manage_locations')

@login_required
def delete_role(request, id):
    try:
        with transaction.atomic():
            role = get_object_or_404(Role, id=id)
            if request.method == 'POST':
                role.delete()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Role deleted successfully'
                })
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid request method'
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error deleting role: {str(e)}'
        }, status=500)

@login_required
def get_location(request, id):
    location = get_object_or_404(Location, id=id)
    return JsonResponse({
        'id': location.id,
        'name': location.name,
        'address': location.address
    })

@login_required
def manage_roles(request):
    roles = Role.objects.all()
    if request.method == 'POST':
        if 'edit' in request.GET:
            role = get_object_or_404(Role, id=request.GET['edit'])
            form = RoleForm(request.POST, instance=role)
        else:
            form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_roles')
    else:
        if 'edit' in request.GET:
            role = get_object_or_404(Role, id=request.GET['edit'])
            form = RoleForm(instance=role)
        else:
            form = RoleForm()
    return render(request, 'manage_roles.html', {'roles': roles, 'form': form})

@login_required
def manage_permissions(request):
    permissions = Permission.objects.all()
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_permissions')
    else:
        form = PermissionForm()
    return render(request, 'manage_permissions.html', {'permissions': permissions, 'form': form})

@login_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@login_required
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
            return redirect('manage_users')
        messages.error(request, 'Error creating user')
        return render(request, 'manage_users.html', {
            'users': User.objects.all(),
            'form': form
        })
    return render(request, 'manage_users.html', {
        'users': User.objects.all(),
        'form': UserForm()
    })

@login_required
def update_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully')
            return redirect('manage_users')
        messages.error(request, 'Error updating user')
    return redirect('manage_users')

@login_required
def delete_user(request, id):
    try:
        with transaction.atomic():
            user = get_object_or_404(User, id=id)
            if request.method == 'POST':
                user.delete()
                messages.success(request, 'User deleted successfully')
                return redirect('manage_users')
            messages.error(request, 'Invalid request method')
            return redirect('manage_users')
    except Exception as e:
        messages.error(request, f'Error deleting user: {str(e)}')
        return redirect('manage_users')

@login_required
def get_user(request, id):
    user = get_object_or_404(User, id=id)
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    })

def access_denied(request):
    return render(request, 'access_denied.html')
