from django.urls import path
from .views import TaxListCreateView, TaxDetailView, InvoiceListCreateView, InvoiceDetailView, InvoiceItemListCreateView, InvoiceItemDetailView

urlpatterns = [
    path('taxes/', TaxListCreateView.as_view(), name='tax-list-create'),
    path('taxes/<int:pk>/', TaxDetailView.as_view(), name='tax-detail'),
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoice-items/', InvoiceItemListCreateView.as_view(), name='invoice-item-list-create'),
    path('invoice-items/<int:pk>/', InvoiceItemDetailView.as_view(), name='invoice-item-detail'),
]