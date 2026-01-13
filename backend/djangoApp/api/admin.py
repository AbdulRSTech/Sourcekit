"""Register `Resource` and `Keyword` models with the Django admin."""
from django.contrib import admin
from .models import Resource, Keyword

# Register models so they are manageable in the admin interface
admin.site.register(Resource)
admin.site.register(Keyword)