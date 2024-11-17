from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User, BankPersonnel, Admin
from .forms import CustomUserAdmin

class BankPersonnelForm(forms.ModelForm):
    class Meta:
        model = BankPersonnel
        fields = ['user']

class BankPersonnelAdmin(admin.ModelAdmin):
    form = BankPersonnelForm
    list_display = ['user', ]


admin.site.register(BankPersonnel, BankPersonnelAdmin)
admin.site.register(User, CustomUserAdmin)
# admin_group = Group.objects.create(name='Admin')
# loan_provider_group = Group.objects.create(name='LoanProvider')
# loan_customer_group = Group.objects.create(name='LoanCustomer')
# bank_personnel_group = Group.objects.create(name='BankPersonnel')