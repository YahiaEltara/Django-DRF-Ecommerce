from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer, CardInformationSerializer
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
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(queryset)
        return Response(serializer.data)
    
    @extend_schema(responses=CategorySerializer)
    def update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(responses=CategorySerializer)
    def create(self, request):
        if Category.objects.filter(name=request.data.get('name')).exists():
            return Response({"error": "A category with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(responses=CategorySerializer)
    def destroy(self, request, pk=None):
        try:
            queryset = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        queryset.delete()
        return Response({"message": "Category is deleted"}, status=status.HTTP_200_OK)





class BrandViewSet(viewsets.ViewSet):
    queryset = Brand.objects.all()
    lookup_field = 'slug'

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(responses=BrandSerializer)
    def retrieve(self, request, slug=None):
        try:
            queryset = Brand.objects.get(slug=slug)
        except Brand.DoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BrandSerializer(queryset)
        return Response(serializer.data)
    
    @extend_schema(responses=BrandSerializer)
    def update(self, request, slug=None):
        try:
            brand = Brand.objects.get(slug=slug)
        except Brand.DoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BrandSerializer(brand, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(responses=BrandSerializer)
    def create(self, request):
        if Brand.objects.filter(name=request.data.get('name')).exists():
            return Response({"error": "A brand with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=BrandSerializer)
    def destroy(self, request, slug=None):
        try:
            queryset = Brand.objects.get(slug=slug)
        except Brand.DoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset.delete()
        return Response({"message": "Brand is deleted"}, status=status.HTTP_200_OK)





class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(responses=ProductSerializer)
    def retrieve(self, request, pk=None):
        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(queryset)
        return Response(serializer.data)
    
    @extend_schema(responses=ProductSerializer)
    def update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=ProductSerializer)
    def create(self, request):
        if Product.objects.filter(name=request.data.get('name')).exists():
            return Response({"error": "A product with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(responses=ProductSerializer)
    def destroy(self, request, pk=None):
        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response( {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset.delete()
        return Response({"message": "Product is deleted"}, status=status.HTTP_200_OK)





import stripe


class PaymentViewSet(viewsets.ViewSet):
    serializer_class = CardInformationSerializer

    def create(self, request):
        """
        Handle payment requests via Stripe.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            stripe.api_key = 'your-stripe-secret-key'
            payment_response = self.process_payment(serializer.validated_data)
            return Response(payment_response, status=payment_response.get('status', status.HTTP_400_BAD_REQUEST))
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def process_payment(self, card_data):
        """
        Process the payment using Stripe API.
        """
        try:
            # Create PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=10000,  # Amount in smallest currency unit (e.g., cents)
                currency='inr',
                payment_method_data={
                    "type": "card",
                    "card": {
                        "number": card_data['card_number'],
                        "exp_month": int(card_data['expiry_month']),
                        "exp_year": int(card_data['expiry_year']),
                        "cvc": card_data['cvc'],
                    },
                },
                confirm=True,
            )

            # Check payment status
            if payment_intent['status'] == 'succeeded':
                return {"message": "Card Payment Success", "status": status.HTTP_200_OK, "payment_intent": payment_intent, }
            else:
                return {"message": "Card Payment Failed", "status": status.HTTP_400_BAD_REQUEST, "payment_intent": payment_intent, }
        except stripe.error.CardError as e:
            # Handle card errors
            return { "error": "Card declined", "status": status.HTTP_400_BAD_REQUEST, "details": str(e.error.message), }
        except Exception as e:
            # Handle other errors
            return {"error": "Payment processing failed", "status": status.HTTP_500_INTERNAL_SERVER_ERROR, "details": str(e), }

