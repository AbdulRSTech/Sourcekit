from django.shortcuts import render

# Create your views here.
def index(request):
    # Serve React's index.html for non API requests
    return render(request, 'index.html')