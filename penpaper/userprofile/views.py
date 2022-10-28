from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Create your views here.
def index(request):
    return "hello"

@require_http_methods(["POST"])
def register(request):
    return JsonResponse({"status":200})
        
