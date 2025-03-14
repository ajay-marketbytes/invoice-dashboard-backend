from django.db import models

class Client(models.Model):
    CLIENT_TAX_CHOICES = [
        ("gst", "GST"),
        ("vat", "VAT"),
        ("nil", "Nil"),
    ]

    client_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    tax_type = models.CharField(max_length=3, choices=CLIENT_TAX_CHOICES)
    gst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    vat = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    website = models.URLField()
    invoice_series = models.CharField(
        max_length=20,
        choices=[("domestic", "Domestic"), ("international", "International")],
    )
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Enforce tax logic based on tax_type
        if self.tax_type == "gst":
            self.vat = 0.00  # Reset VAT to 0 if GST is selected
        elif self.tax_type == "vat":
            self.gst = 0.00  # Reset GST to 0 if VAT is selected
        else:  # tax_type is "nil"
            self.gst = 0.00
            self.vat = 0.00
        super().save(*args, **kwargs)

    def __str__(self):
        return self.client_name