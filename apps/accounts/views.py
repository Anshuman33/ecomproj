from django.http import HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from .models import User, Buyer, Seller
from django.contrib.auth import login as djlogin, authenticate
from django.views.decorators.csrf import csrf_exempt
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
            buyer = Buyer(user = user)
            buyer.save()
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
        if 'email' in params and 'password' in params:
            user = authenticate(request, username=params['email'], password=params['password'])
            if user is not None:
                djlogin(request, user)
                return JsonResponse({"status":200, "msg" : "User successfully logged in"})
            else:
                return JsonResponse({"status":401, "msg" : "Invalid username or password"})
            
        else:
            return JsonResponse({'status':401, "msg" : "Empty username or password"}) 

@csrf_exempt
def registerUserAsSeller(request):
    if request.method == "POST":
        user = request.user
        if not user.is_seller:
            user.is_seller = True
            user.save()
            seller = Seller(user=user)
            seller.save()
            return JsonResponse({"status" : 200, "msg" : "User successfully registered as seller"})
        else:
            return JsonResponse({"status" : 409, "msg" : "User already registered as seller"})
    else:
        return JsonResponse({"status":405, "msg" : "Method not allowed."})

            
        

        
        
    
        
        
