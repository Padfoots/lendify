from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import User, Admin, BankPersonnel, LoanProvider, LoanCustomer


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            if user.user_type == 'admin':
                Admin.objects.create(user=user)
            elif user.user_type == 'bank_personnel':
                BankPersonnel.objects.create(user=user)
            elif user.user_type == 'loan_provider':
                LoanProvider.objects.create(user=user)
            elif user.user_type == 'loan_customer':
                LoanCustomer.objects.create(user=user)

        return user


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ['username', 'email', 'user_type', 'is_active', 'is_staff']
    list_filter = ['user_type', 'is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'user_type')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'user_type', 'first_name', 'last_name', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ['username', 'email']
    ordering = ['username']



