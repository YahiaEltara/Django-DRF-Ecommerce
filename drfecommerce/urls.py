from django.contrib import admin
from django.urls import path, include
from drfecommerce.product import views
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('brand', views.BrandViewSet)
router.register('product', views.ProductViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    # API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name= 'schema'), 
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')), 

    # ViewSets
    path('api/', include(router.urls)),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

