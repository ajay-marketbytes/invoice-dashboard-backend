from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=255)  # Service name (like "Web Design")

    def __str__(self):
        return self.name