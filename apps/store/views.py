from django.shortcuts import render, HttpResponse
from . import api
from .models import CategoryFeature, Category
from .serializers import CategoryFeatureSerializer,CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, json

from rest_framework import status
from rest_framework import permissions
# Create your views here.
def home(request):
    context = {} # Processing to be done
    return HttpResponse(render(request, "home.html", context = context))


def productDetails(request, id):
    response = api.getProductFromId(request, id)
    context = {"response":response}
    return HttpResponse(render(request, "product.html", context=context))




