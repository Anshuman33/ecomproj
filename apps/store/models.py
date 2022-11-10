from django.db import models
from apps.accounts.models import User, Seller, Buyer


class Category(models.Model):
    DEFAULT_CATEGORY = "Generic"
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=30, unique = True, default = DEFAULT_CATEGORY)

class Product(models.Model):
    id = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length = 200, null=False, blank = False)
    seller = models.ForeignKey(Seller, on_delete = models.CASCADE, null=False)
    stock_quantity = models.IntegerField(null=False, default = 0)
    price = models.FloatField(null = False),
    brand = models.CharField(max_length = 100)
    category = models.ForeignKey(Category, on_delete = models.SET_DEFAULT, default=Category.DEFAULT_CATEGORY)
    thumbnail = models.ImageField(upload_to = "uploads/products/", null = True)
    description = models.TextField()



class CategoryFeature(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    feature = models.CharField(max_length = 30, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ["category", "feature"], name="unique_category_feature_combination")
        ]

class ProductFeature(models.Model):
    
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    feature = models.CharField(max_length = 30, null = False)
    value = models.CharField(max_length = 50, null = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ["product", "feature"], name="unique_product_feature_combination")
        ]



