from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import Count, Q 
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

from .models import Resource, Keyword
from .utils import get_resource_info, download_mp3, download_mp4

import json
from datetime import datetime
import requests

"""Views for the `api` app."""

def index(request):
    """Serve the React single-page application for non-API routes.

    Args:
        request (HttpRequest): Django request object.

    Returns:
        HttpResponse: Renders the React `index.html` page.
    """
    # Serve React's `index.html` for non-API requests
    return render(request, 'index.html')

# Add this new endpoint to get CSRF token
@ensure_csrf_cookie
def get_csrf_token(request):
    """Return CSRF token for the frontend"""
    return JsonResponse({'csrfToken': get_token(request)})

