# admin.py
from django.contrib import admin
from .models import Customer, LoanData

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'monthly_income', 'approved_limit', 'current_debt')
    search_fields = ['first_name', 'last_name', 'phone_number']

class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'customer', 'loan_amount', 'interest_rate', 'monthly_repayment', 'emis_paid_on_time', 'start_date', 'end_date')
    list_filter = ('customer', 'interest_rate', 'emis_paid_on_time')
    search_fields = ['customer__first_name', 'customer__last_name', 'loan_amount']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(LoanData, LoanAdmin)
