from rest_framework import generics
from .models import Tax, Invoice, InvoiceItem
from .serializers import TaxSerializer, InvoiceSerializer, InvoiceItemSerializer
from rest_framework.permissions import AllowAny

class TaxListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer

class TaxDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer

class InvoiceListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer

class InvoiceItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer