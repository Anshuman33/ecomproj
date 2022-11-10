
from django.http import HttpRequest, JsonResponse
# from django.db.utils import 
from .models import Product, CategoryFeature, Category, ProductFeature
from .serializers import ProductSerializer, CategorySerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, json
from rest_framework import status
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import json

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_seller

class CategoryApiView(APIView):
    # permission to check whether user is authenticated
    permission_classes = [IsReadOnly | permissions.IsAdminUser]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    def get(self, request, category_id = None, *args, **kwargs):
        # category_id = kwargs.get("category_id")
        print(request.user)
        if category_id is None:
            categories = Category.objects.all()
            data = CategorySerializer(categories, many=True).data
            return Response(data=data, status = status.HTTP_200_OK)
        else:
            try:
                category = Category.objects.get(id = category_id)
                data = CategorySerializer(category).data
                return Response(data=data, status = status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response(data = {'msg' : "Resource doesn't exist."}, status = status.HTTP_404_NOT_FOUND)

    def post(self, request):
        params = json.loads(request.body)
        serializer = CategorySerializer(data = params)
        serializer.is_valid()
        # print(serializer.is_valid())
        # print(serializer.validated_data)
        # print(serializer.errors)
        serializer.save()
        return Response({"msg":"Category added successfully."}, status.HTTP_201_CREATED)

    def delete(self, request, category_id):
        try:
            category = Category.objects.find(id = category_id)
            category.delete()
            return Response({"msg" : "Category successfully deleted"}, status = status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"msg" : "Category does not exist"}, status = status.HTTP_404_NOT_FOUND)




class ProductsApiView(APIView):
    permission_classes = [IsReadOnly | IsSeller | permissions.IsAdminUser]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    def get(self, request, products_id = None):
        if products_id is None:
            products = Product.objects.all()
            data = ProductSerializer(products, many = True).data
            return Response(data = data, status = status.HTTP_200_OK)
        else:
            try:
                product = Product.objects.find(products_id).first()
                data = ProductSerializer(product).data
                return Response(data = data, status = status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response(data = {'msg': "Resource does not exist"}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request):
        params = json.loads(request.body)
        params['seller'] = request.user
        serializer = ProductSerializer(data = params)
        serializer.is_valid()
        print(serializer._errors)
        serializer.save()
        return Response(data={'msg' : "Product added successfully."}, status = status.HTTP_201_CREATED)
        


def products(request : HttpRequest, product_id = None):
    if request.method == "GET":
        if product_id is None:
            products = Product.objects.all()
            serializer = ProductSerializer(products)
            return JsonResponse({"status":200, "data":serializer.data})
        else:
            product = Product.objects.get(id = id).first()
            if product is not None:
                serializer = ProductSerializer(product)
                return JsonResponse({"status":200, "data":serializer.data})
            else:
                return JsonResponse({"status":404, "data": {"msg" : "Product not found"}})

    elif request.method == "POST":
        user = request.user
        if user.is_authenticated() and user.is_seller:
            params = request.POST.dict()
            prodName = params.get("prodName")
            categoryName = params.get('categoryName')
            features = params.get("features")
            stock_quantity = params.get("stockQuantity")
            price = params.get('price')
            brand = params.get('brand')
            description = params.get('description')

            seller = user.seller
            category = Category.objects.get(name = categoryName)
            
            product = Product(name = prodName, 
                            seller = seller, 
                            stock_quantity = stock_quantity,
                            price = price,
                            brand = brand,
                            category = category,
                            description = description
                            )
            product.save()
            if features:
                for feature, value in features.items():
                    product.productfeature_set.create(feature = feature, value = value)

            return JsonResponse({"status":200, "msg":"Product added successfully"})
        else:
            return JsonResponse({"status": 403, "msg":"Access forbidden to this user."})


def getProductFromId(request, id):

    product = Product.objects.get(id = id).first()
    if product is not None:
        serializer = ProductSerializer(product)
        return JsonResponse({"status":200, "data":serializer.data})
    else:
        return JsonResponse({"status":404, "data": {"msg" : "Product not found"}})

