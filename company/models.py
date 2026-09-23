import re
from django import forms
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class FiscalYear(models.Model):
    name                                        = models.CharField(max_length=100, unique=True)  
    start_from                                  = models.CharField(max_length=100,null=True,blank=True)
    end_date                                    = models.CharField(max_length=100,null=True,blank=True)
    status                                      = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Closed', 'Closed')], default='Active')
    created_at                                  = models.DateTimeField(auto_now_add=True)
    updated_at                                  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering                                = ['-start_from']  
        indexes                                 = [models.Index(fields=['name'])]  

    def __str__(self):
        return f"{self.name} ({self.start_from} - {self.end_date})"


class Company(models.Model):
    fiscal_year                                 = models.ForeignKey(FiscalYear, on_delete=models.PROTECT, related_name="companies")
    name                                        = models.CharField(max_length=100, unique=True)  
    print_name                                  = models.CharField(max_length=100, blank=True, null=True)
    fiscal_year_beginning_from                  = models.CharField(max_length=100,null=True,blank=True)
    book_commencing_from                        = models.CharField(max_length=100,null=True,blank=True)
    address                                     = models.TextField(blank=True, null=True) 
    pan                                         = models.CharField(max_length=50, blank=True, null=True, unique=True)
    phone                                       = models.CharField(max_length=20, blank=True, null=True,validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")])
    email                                       = models.EmailField(blank=True, null=True, unique=True)
    image                                       = models.ImageField(upload_to='company/logo/', blank=True, null=True)
    created_at                                  = models.DateTimeField(auto_now_add=True)
    updated_at                                  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering                                = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['fiscal_year']),
        ]
    def __str__(self):
        return self.name
    @property
    def company_logo_URL(self):
        return self.image.url if self.image else ''
    
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def clean_pan(self):
        pan = self.cleaned_data.get('pan')
        if pan and Company.objects.filter(pan=pan).exists():
            raise ValidationError("This PAN number is already registered.")
        return pan

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\+?1?\d{10}$', phone):
            raise ValidationError("Enter a valid phone number.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Company.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean(self):
        if (fiscal_year := self.cleaned_data.get('fiscal_year')) and fiscal_year.status != 'Active':
            raise ValidationError("The selected fiscal year is not active.")
        return self.cleaned_data