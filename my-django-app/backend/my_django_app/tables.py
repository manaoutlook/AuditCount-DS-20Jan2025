import django_tables2 as tables
from .models import Location

class LocationTable(tables.Table):
    class Meta:
        model = Location
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "name")