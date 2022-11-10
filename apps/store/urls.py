from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from . import api

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.productDetails, name="productDetails"),
    path('api/products/', api.ProductsApiView.as_view(),name="productApi"),
    path('api/products/<int:id>', api.getProductFromId, name="productDetailsApi"),
    path('api/categories/', csrf_exempt(api.CategoryApiView.as_view()), name="categoryApiAll"),
    path('api/categories/<int:category_id>', csrf_exempt(api.CategoryApiView.as_view()), name="categoryApi")
]