from django.contrib import admin
from .models import User, Role, Location, Permission

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Location)
admin.site.register(Permission)
