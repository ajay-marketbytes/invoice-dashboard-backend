from django.db import models
 
# Create your models here.
 
 
class BranchAddress(models.Model):
    branch_address = models.TextField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    gstin = models.CharField(max_length=15)
    phone_code = models.CharField(max_length=5, default='+91')
    phone = models.CharField(max_length=15)
    website = models.URLField()
 
    def __str__(self):
        return f"{self.branch_address}, {self.city}, {self.state}"
   
 