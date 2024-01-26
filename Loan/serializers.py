# appname/serializers.py
from rest_framework import serializers
from .models import Customer, LoanData

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanData
        fields = '__all__'
