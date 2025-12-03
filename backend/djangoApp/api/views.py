from django.shortcuts import render

from .models import Resource, Keyword
from utils import download_mp3, download_mp4

# Create your views here.
def index(request):
    # Serve React's index.html for non API requests
    return render(request, 'index.html')