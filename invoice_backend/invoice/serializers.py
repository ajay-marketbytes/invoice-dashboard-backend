from rest_framework import serializers
from .models import Tax, Invoice, InvoiceItem

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['id', 'name', 'percentage']

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'invoice', 'item_type', 'product', 'name', 'quantity', 'unit_cost', 'total', 'total_gst']
        read_only_fields = ['total', 'total_gst']

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'final_invoice_number', 'invoice_type', 'client', 'branch_address', 'bank_account',
            'invoice_date', 'due_date', 'currency_type', 'payment_terms', 'tax_option', 'tax_rate',
            'subtotal', 'gst', 'discount', 'shipping', 'amount_paid', 'total_due', 'items', 'is_final', 'is_saved_final'
        ]
        read_only_fields = ['invoice_number', 'final_invoice_number', 'subtotal', 'gst', 'total_due']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        instance = super().update(instance, validated_data)
        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                InvoiceItem.objects.create(invoice=instance, **item_data)
        instance.calculate_totals()
        instance.save()
        if instance.is_final:
            instance.generate_final_invoice_number()
        return instance