from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

from .models import Resource, Keyword
from .utils import download_mp3, download_mp4

import json
from datetime import datetime

# Create your views here.
def index(request):
    # Serve React's index.html for non API requests
    return render(request, 'index.html')

# Add this new endpoint to get CSRF token
@ensure_csrf_cookie
def get_csrf_token(request):
    """Return CSRF token for the frontend"""
    return JsonResponse({'csrfToken': get_token(request)})

# save keyword 
def saveKeyword(request, word):
    if request.method == "POST":
        word = word.lower().strip()

        if not word:
            return JsonResponse({"error": "No word entered"}, status=400)

        try:
            # Use get_or_create instead of filter
            keyword, created = Keyword.objects.get_or_create(keyword=word)
            if created:
                return JsonResponse({"success": "Created and added keyword"}, status=200)
            else:
                return JsonResponse({"success": "Added existing keyword"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": f"Error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def save(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            title = data.get("title", "").strip().title()
            url = data.get("url", "").strip()
            filename = data.get("filename", "").strip()
            keywords = data.get("keywords", [])  # This should be a list
            notes = data.get("notes", "").strip()

            # Fixed validation logic
            if not title or not url or not filename or not notes:
                return JsonResponse({"error": "All fields must be filled"}, status=400)

            # create resource
            resource = Resource.objects.create(
                title=title,
                url=url,
                filename=filename,
                notes=notes,
                date_added=datetime.today()
            )

            # Loop over each keyword
            for keyword_text in keywords:
                keyword_text = keyword_text.lower().strip()
                if keyword_text:
                    keyword, _ = Keyword.objects.get_or_create(keyword=keyword_text)
                    resource.keywords.add(keyword)
            
            return JsonResponse({"success": "Saved"}, status=200)

        except IntegrityError as e:
            return JsonResponse({"error": f"Database error: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def saveAndDownload(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            title = data.get("title", "").strip().title()
            url = data.get("url", "").strip()
            filename = data.get("filename", "").strip()
            keywords = data.get("keywords", [])
            notes = data.get("notes", "").strip()
            desired_format = data.get("format", "").lower().strip()

            if not title or not url or not filename or not notes or not desired_format:
                return JsonResponse({"error": "All fields must be filled"}, status=400)

            # create resource
            resource = Resource.objects.create(
                title=title,
                url=url,
                filename=filename,
                notes=notes,
                date_added=datetime.today()
            )

            # Loop over each keyword
            for keyword_text in keywords:
                keyword_text = keyword_text.lower().strip()
                if keyword_text:
                    keyword, _ = Keyword.objects.get_or_create(keyword=keyword_text)
                    resource.keywords.add(keyword)
            
            # Download in desired format
            if desired_format == "mp3":
                downloaded = download_mp3(url, filename)
                if downloaded["success"] is True:
                    resource.date_downloaded = datetime.today()
                    resource.save()
                    return JsonResponse({"success": "Saved and Downloaded", "download": downloaded}, status=200)
                else:
                    return JsonResponse({"error": "Error downloading mp3"}, status=500)

            elif desired_format == "mp4":
                downloaded = download_mp4(url, filename)
                if downloaded["success"] is True:
                    resource.date_downloaded = datetime.today()
                    resource.save()
                    return JsonResponse({"success": "Saved and Downloaded", "download": downloaded}, status=200)
                else:
                    return JsonResponse({"error": "Error downloading mp4"}, status=500)

            else:
                return JsonResponse({"error": "Not a supported format"}, status=400)

        except IntegrityError as e:
            return JsonResponse({"error": f"Database error: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def download(request, id, format):
    if request.method != "GET" and request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    if not format:
        return JsonResponse({"error": "No format specified"}, status=400)
    
    format = format.lower()

    try: 
        resource = Resource.objects.get(id=id)
        
        if format == "mp3":
            downloaded = download_mp3(resource.url, resource.filename)
            if downloaded["success"] is True:
                resource.date_downloaded = datetime.today()
                resource.save()
                return JsonResponse(downloaded, status=200)
            else:
                return JsonResponse({"error": "Failed to download mp3"}, status=500)

        elif format == "mp4":
            downloaded = download_mp4(resource.url, resource.filename)
            if downloaded["success"] is True:
                resource.date_downloaded = datetime.today()
                resource.save()
                return JsonResponse(downloaded, status=200)
            else:
                return JsonResponse({"error": "Failed to download mp4"}, status=500)

        else:
            return JsonResponse({"error": "Format not supported"}, status=400)

    except Resource.DoesNotExist:
        return JsonResponse({"error": "This resource does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error: {str(e)}"}, status=500)
    
def delete(request, id):
    if request.method != "DELETE" and request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        resource = Resource.objects.get(id=id)
        resource.delete()
        return JsonResponse({"data": "Resource deleted"}, status=200)

    except Resource.DoesNotExist:
        return JsonResponse({"error": "Resource does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Error: {str(e)}"}, status=500)