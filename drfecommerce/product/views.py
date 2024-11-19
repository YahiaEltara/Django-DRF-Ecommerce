from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(responses=CategorySerializer)
    def retrieve(self, request, pk=None):
        try:
            queryset = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CategorySerializer(queryset)
        return Response(serializer.data)
    
    @extend_schema(responses=CategorySerializer)
    def update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(responses=CategorySerializer)
    def create(self, request):
        parent_id = request.data.get('parent')
        parent = None
        if parent_id:
            try:
                parent = Category.objects.get(pk=parent_id)
            except Category.DoesNotExist:
                return Response(
                    {"error": "Parent category not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
        category = Category.objects.create(name=request.data['name'],
                                           parent = parent)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class BrandViewSet(viewsets.ViewSet):
    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(responses=BrandSerializer)
    def retrieve(self, request, pk=None):
        try:
            queryset = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Brand not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = BrandSerializer(queryset)
        return Response(serializer.data)
    
    @extend_schema(responses=BrandSerializer)
    def update(self, request, pk=None):
        try:
            brand = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Brand not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = BrandSerializer(brand, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(responses=BrandSerializer)
    def create(self, request):
        brand_name = request.data.get('name')
        brand = None
        try:
            brand = Brand.objects.get(name=brand_name)
        except Brand.DoesNotExist:     
            brand = Brand.objects.create(name=request.data['name'])
            serializer = BrandSerializer(brand, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        




class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    
    @extend_schema(responses=ProductSerializer)
    def create(self, request):
        brand_name = request.data.get('brand')
        category_name = request.data.get('category')
        product = None

        if brand_name and category_name:
            try:
                brand = Brand.objects.get(name=brand_name)
                category = Category.objects.get(name=category_name)
            except Brand.DoesNotExist:
                return Response(
                    {"error": f"Brand with name '{brand_name}' not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Category.DoesNotExist:
                return Response(
                    {"error": f"Category with name '{category_name}' not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            product = Product.objects.create(
                name=request.data['name'],
                description=request.data.get('description', ''),
                is_digital=request.data.get('is_digital', False),
                brand=brand,
                category=category
            )
            return Response(
                {"message": "Product created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"error": "Both brand and category names are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

