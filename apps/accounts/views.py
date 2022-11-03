from django.http import HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from .models import User
from django.contrib.auth import login as djlogin, authenticate

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
        params = request.POST
        # print(params)
        if 'email' in params and 'password' in params:
            user = authenticate(request, username=params['email'], password=params['password'])
            if user is not None:
                djlogin(request, user)
                return JsonResponse({"status":200, "msg" : "User successfully logged in"})
            else:
                return JsonResponse({"status":401, "msg" : "Invalid username or password"})
            
        else:
            return JsonResponse({'status':401, "msg" : "Empty username or password"}) 
            
        

        
        
    
        
        
