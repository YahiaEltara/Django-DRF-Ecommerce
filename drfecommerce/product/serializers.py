from rest_framework import serializers
from .models import Category, Brand, Product




        
class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.ReadOnlyField(source = 'brand.name')
    category = serializers.ReadOnlyField(source = 'category.name')
    class Meta:
        model = Product
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude_fields = ['id']
        for field in exclude_fields:
            self.fields.pop(field, None)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.ReadOnlyField(source='parent.name')
    products = ProductSerializer(many = True, read_only = True)

    class Meta:
        model = Category
        fields = ['name', 'parent', 'products']

