from rest_framework import serializers
from .models import Product, Category, CategoryFeature, ProductFeature

class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['feature', 'value']

class ProductSerializer(serializers.ModelSerializer):
    features = ProductFeatureSerializer(source='productfeature_set', many = True)
    
    class Meta:
        model = Product
        fields = '__all__' 

    def create(self, validated_data):
        features_data = validated_data.pop('productfeature_set')
        product = Product.objects.create(**validated_data)
        for feature in features_data:
            product.productfeature_set.create(**feature)
        return product
    
class CategoryFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryFeature
        fields = ['feature']

class CategorySerializer(serializers.ModelSerializer):
    features = CategoryFeatureSerializer(source='categoryfeature_set', many=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'features']

    def create(self, validated_data):
        features_data = validated_data.pop('categoryfeature_set')
        category = Category.objects.create(**validated_data)
        for feature in features_data:
            category.categoryfeature_set.create(**feature)
        return category