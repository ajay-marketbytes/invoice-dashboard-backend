from django.db import models

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.percentage}%"

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=255, unique=True)
    invoice_type = models.CharField(max_length=50, choices=[("product", "Product"), ("service", "Service")])
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    branch_address = models.ForeignKey('Branchaddress.BranchAddress', on_delete=models.CASCADE)
    bank_account = models.ForeignKey('bankaccount.BankAccount', on_delete=models.CASCADE)
    invoice_date = models.DateField()
    due_date = models.DateField()
    currency_type = models.CharField(max_length=10)
    payment_terms = models.CharField(max_length=50)
    tax_option = models.CharField(max_length=3, choices=[("yes", "Yes"), ("no", "No")], default="no")
    tax_rate = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_totals(self):
        self.subtotal = sum(item.quantity * item.unit_cost for item in self.items.all())
        if self.tax_option == "yes" and self.tax_rate:
            self.gst = (self.subtotal * self.tax_rate.percentage) / 100
        else:
            self.gst = 0
        self.total_due = self.subtotal + self.gst - self.discount + self.shipping - self.amount_paid

    def save(self, *args, **kwargs):
        # Generate invoice number if not set
        if not self.invoice_number:
            last_invoice = Invoice.objects.order_by("-id").first()
            new_number = int(last_invoice.invoice_number.split("-")[-1]) + 1 if last_invoice else 1
            self.invoice_number = f"INV-{str(new_number).zfill(5)}"
        super().save(*args, **kwargs)  # Save without calculating totals here

    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.client}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    item_type = models.CharField(max_length=20, choices=[("product", "Product"), ("service", "Service")])
    product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    total_gst = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.item_type == "product" and self.product:
            self.name = self.product.name
            self.unit_cost = self.product.unit_cost
        if self.invoice.tax_option == "yes" and self.invoice.tax_rate:
            self.total_gst = (self.quantity * self.unit_cost * self.invoice.tax_rate.percentage) / 100
        else:
            self.total_gst = 0
        self.total = self.quantity * self.unit_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.quantity})"

# Placeholder models (remove or replace with actual imports if apps exist)
class Client(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class BranchAddress(models.Model):
    address = models.TextField()
    def __str__(self):
        return self.address[:50]

class BankAccount(models.Model):
    account_number = models.CharField(max_length=50)
    def __str__(self):
        return self.account_number

class Product(models.Model):
    name = models.CharField(max_length=255)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name