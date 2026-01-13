from django.db import models

class Resource(models.Model):
    """A saved media resource with descriptive metadata.

    Fields:
      - title: human-friendly unique title
      - url: original source URL
      - filename: desired filename for downloads (unique)
      - notes: optional free-form notes about the resource
      - aspect_ratio/resolution/video_quality/audio_quality: extracted metadata
      - date_added and date_downloaded: tracking dates for creation and download
    """

    title = models.CharField(max_length=100, null=False, unique=True)
    url = models.URLField(null=False, unique=True)
    filename = models.CharField(max_length=100, null=False, unique=True)
    notes = models.TextField(null=True, blank=True)
    aspect_ratio = models.TextField(null=True, blank=True)
    resolution = models.TextField(null=True, blank=True)
    video_quality = models.TextField(null=True, blank=True)
    audio_quality = models.TextField(null=True, blank=True)
    date_added = models.DateField(null=False)
    date_downloaded = models.DateField(null=True, blank=True)


class Keyword(models.Model):
    """Keyword that can be attached to multiple `Resource` objects.

    Stores a unique keyword string and links to `Resource` via a
    `ManyToManyField`. The related name on `Resource` is `keywords`.
    """
    
    resources = models.ManyToManyField(Resource, related_name="keywords")
    keyword = models.CharField(null=True, blank=True, max_length=50, unique=True)