from django.db import models

# Create your models here.

# Resource model
class Resource(models.Model):
    title = models.CharField(max_length=100, null=False, unique=True)
    url = models.URLField(null=False, unique=True)
    filename = models.CharField(max_length=100, null=False, unique=True)
    notes = models.TextField(null=True, blank=True)
    date_added = models.DateField(null=False)
    date_downloaded = models.DateField(null=True, blank=True)

# Keyword model
class Keyword(models.Model):
    resources = models.ManyToManyField(Resource, related_name="keywords")
    keyword = models.CharField(null=True, blank=True, max_length=50, unique=True)