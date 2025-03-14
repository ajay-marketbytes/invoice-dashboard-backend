from django.shortcuts import render
 
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import BranchAddress
from .serializers import BranchAddressSerializer
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
 
class BranchAddressViewSet(viewsets.ModelViewSet):
    permission_classes=[AllowAny]

    queryset = BranchAddress.objects.all()
    serializer_class = BranchAddressSerializer
 
    # List all branch addresses (GET)
    def list(self, request, *args, **kwargs):
        branch_addresses = self.get_queryset()
        serializer = self.get_serializer(branch_addresses, many=True)
        return Response(serializer.data)
 
    # Retrieve a specific branch address (GET)
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NotFound:
            return Response({"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND)
       
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
 
    # Create a new branch address (POST)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    # Update an existing branch address (PUT/PATCH)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NotFound:
            return Response({"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND)
 
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    # Delete a branch address (DELETE)
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NotFound:
            return Response({"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND)
       
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 