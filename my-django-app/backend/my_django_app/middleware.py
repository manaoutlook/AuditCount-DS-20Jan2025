from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedAccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Implement role-based access control logic here
        # Example: if not request.user.has_role('admin'):
        #              return HttpResponseForbidden()
        return self.get_response(request)

class LocationBasedAccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_location = request.user.location
            # Add your location-based access control logic here
            if user_location and user_location.name != 'Allowed Location':
                return redirect(reverse('access_denied'))
        response = self.get_response(request)
        return response
