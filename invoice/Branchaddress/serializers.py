 
from rest_framework import serializers
from .models import BranchAddress
 
class BranchAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchAddress
        fields = ['id', 'branch_address', 'state', 'city', 'gstin', 'phone_code', 'phone', 'website']
 