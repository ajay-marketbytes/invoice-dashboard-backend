from django.contrib import admin
from .models import Product

# Create a custom ProductAdmin class to configure how the Product model appears in the admin interface
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit_cost')  # Columns to display in the list view
    search_fields = ('name',)  # Allows searching by product name
    list_filter = ('unit_cost',)  # Allows filtering by price
    ordering = ('name',)  # Default ordering by product name
    list_per_page = 10  # Number of products to display per page in the admin interface

# Register the Product model with the custom admin configuration
admin.site.register(Product, ProductAdmin)
