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
        read_only_fields = ['invoice', 'total', 'total_gst']
        extra_kwargs = {
            'name': {'required': False},
            'unit_cost': {'required': False}
        }
 
    def validate(self, data):
        item_type = data.get('item_type')
        product = data.get('product')
        if item_type == 'product' and not product:
            raise serializers.ValidationError("Product is required for product-type items.")
        if item_type == 'service' and product:
            raise serializers.ValidationError("Product should not be specified for service-type items.")
        return data
 
class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, required=False)
 
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'invoice_type', 'client', 'branch_address', 'bank_account',
            'invoice_date', 'due_date', 'currency_type', 'payment_terms', 'tax_option', 'tax_rate',
            'subtotal', 'gst', 'discount', 'shipping', 'amount_paid', 'total_due', 'items'
        ]
        read_only_fields = ['invoice_number', 'subtotal', 'gst', 'total_due']
 
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            serializer = InvoiceItemSerializer(data=item_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(invoice=invoice)
        invoice.calculate_totals()
        invoice.save()
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
        return instance