from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BranchAddressViewSet
 
router = DefaultRouter()
router.register('branch_addresses', BranchAddressViewSet)
 
urlpatterns = [
    path('', include(router.urls)),
]
 