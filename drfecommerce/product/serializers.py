from rest_framework import serializers
from .models import Category, Brand, Product




        
class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(queryset=Brand.objects.all(), slug_field='name')
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')

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
    parent = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    products = ProductSerializer(many = True, read_only = True)

    class Meta:
        model = Category
        fields = ['name', 'parent', 'products']

