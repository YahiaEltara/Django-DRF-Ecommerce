from django.contrib import admin
from django.urls import path, include
from drfecommerce.product import views
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()
router.register('category', views.CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name= 'schema'), 
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')), 

    # ViewSets
    path('api/', include(router.urls)),

]

