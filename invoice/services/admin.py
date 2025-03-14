from django.contrib import admin
from .models import Service

# Create a custom ServiceAdmin class to configure how the Service model appears in the admin interface
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Columns to display in the list view
    search_fields = ('name',)  # Allows searching by service name
    ordering = ('name',)  # Default ordering by service name
    list_per_page = 10  # Number of services to display per page in the admin interface
admin.site.register(Service, ServiceAdmin)