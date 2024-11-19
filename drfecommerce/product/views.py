from .models import Category
from .serializers import CategorySerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer_data = CategorySerializer(self.queryset, many=True).data
        return Response(serializer_data)
    
    @extend_schema(responses=CategorySerializer)
    def retrieve(self, request, pk=None):
        try:
            queryset = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer_data = CategorySerializer(queryset).data
        return Response(serializer_data)
    
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




