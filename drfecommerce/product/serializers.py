from rest_framework import serializers
from .models import Category, Brand, Product
import datetime




        
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



def validate_expiry_month(value):
    if not 1 <= int(value) <= 12:
        raise serializers.ValidationError("Invalid expiry month.")


def validate_expiry_year(value):
    current_year = datetime.datetime.now().year
    if int(value) < current_year:
        raise serializers.ValidationError("Invalid expiry year.")


def validate_cvc(value):
    if not 3 <= len(value) <= 4 or not value.isdigit():
        raise serializers.ValidationError("Invalid CVC number.")


class CardInformationSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, min_length=13, required=True)
    expiry_month = serializers.CharField(max_length=2, required=True, validators=[validate_expiry_month])
    expiry_year = serializers.CharField(max_length=4, required=True, validators=[validate_expiry_year])
    cvc = serializers.CharField(max_length=4, required=True, validators=[validate_cvc])
