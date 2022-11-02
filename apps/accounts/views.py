from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import render
from .models import User

# Create your views here.
def register(request):
    if request.method == "GET":
        context = {}
        return render(request, "register.html", context)
    elif request.method == "POST":
        params = request.POST.dict()
        params.pop('csrfmiddlewaretoken')
        try:
            user = User.objects.create_user(**params)
            user.save()
        except Exception as e:
            print(e)
            return HttpResponseServerError("Something unexpected happened.")
        return JsonResponse({"status":200, "message": "User successfully registered."})
    
def login(request):
    if request.method == "GET":
        context = {}
        return render(request, 'login.html', context)
    elif request.method == "POST":
        
        
    
        
        
