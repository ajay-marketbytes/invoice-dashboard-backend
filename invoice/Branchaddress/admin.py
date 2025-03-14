
from django.contrib import admin
 
# Register your models here.
from .models import BranchAddress
 
class BranchAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch_address', 'city', 'state', 'gstin', 'phone', 'website')  # Columns to display in list view
    search_fields = ('branch_address', 'city', 'state', 'gstin')  # Fields that can be searched in admin panel
    list_filter = ('state', 'city')  # Filters for sidebar based on state or city
 
# Register the BranchAddress model with the custom BranchAddressAdmin
admin.site.register(BranchAddress, BranchAddressAdmin)
 