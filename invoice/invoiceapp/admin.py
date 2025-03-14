from django.contrib import admin
from .models import Tax, Invoice, InvoiceItem

# Register Tax model
@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'id')
    list_filter = ('percentage',)
    search_fields = ('name',)
    ordering = ('name',)

# Inline for InvoiceItem to show within Invoice admin
class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1  # Number of empty rows to display
    fields = ('item_type', 'product', 'name', 'quantity', 'unit_cost', 'total', 'total_gst')
    readonly_fields = ('total', 'total_gst')  # These are calculated
    can_delete = True

# Register Invoice model with InvoiceItem inline
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number', 'invoice_type', 'client', 'invoice_date', 'due_date',
        'subtotal', 'gst', 'discount', 'shipping', 'amount_paid', 'total_due'
    )
    list_filter = ('invoice_type', 'tax_option', 'currency_type', 'payment_terms')
    search_fields = ('invoice_number', 'client__name')
    date_hierarchy = 'invoice_date'
    inlines = [InvoiceItemInline]
    readonly_fields = ('invoice_number', 'subtotal', 'gst', 'total_due')  # Calculated fields
    fieldsets = (
        (None, {
            'fields': ('invoice_number', 'invoice_type', 'client', 'branch_address', 'bank_account')
        }),
        ('Dates', {
            'fields': ('invoice_date', 'due_date')
        }),
        ('Payment Details', {
            'fields': ('currency_type', 'payment_terms', 'tax_option', 'tax_rate')
        }),
        ('Financials', {
            'fields': ('subtotal', 'gst', 'discount', 'shipping', 'amount_paid', 'total_due')
        }),
    )
    ordering = ('-invoice_date',)

# Register InvoiceItem model separately (optional)
@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'item_type', 'product_name', 'name', 'quantity', 'unit_cost', 'total', 'total_gst')
    list_filter = ('item_type', 'invoice__tax_option')
    search_fields = ('name', 'invoice__invoice_number', 'product__name')
    readonly_fields = ('total', 'total_gst')
    list_select_related = ('invoice', 'product')  # Optimize queries
    ordering = ('-id',)

    def invoice_number(self, obj):
        return obj.invoice.invoice_number
    invoice_number.short_description = "Invoice #"

    def product_name(self, obj):
        return obj.product.name if obj.product else "N/A"
    product_name.short_description = "Product"