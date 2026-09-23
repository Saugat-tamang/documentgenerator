from django.db import models
from company.models import FiscalYear

class ClientRegistration(models.Model):
    name                            = models.CharField(max_length=200,null=True,blank=True)
    address                         = models.CharField(max_length=250,null=True,blank=True)
    pan                             = models.CharField(max_length=30,blank=True,null=True)
    client_code                     = models.CharField(max_length=30,blank=True,null=True)
    phone                           = models.CharField(max_length=30,blank=True,null=True)
    email                           = models.EmailField(max_length=25,blank=True,null=True)
    logo                            = models.FileField(upload_to='images/logo/',null=True,default=True)
    sign                            = models.FileField(upload_to='images/sign/',null=True,default=True)
    stamp                           = models.FileField(upload_to='images/stamp/',null=True,default=True)
    company_id                      = models.PositiveIntegerField(null=True,default=0)
    user_id                         = models.PositiveIntegerField(null=True)
    created_at                      = models.DateTimeField(auto_now_add=True)
    updated_at                      = models.DateTimeField(auto_now=True)
    fiscal_year                     = models.ForeignKey(FiscalYear, null=True, blank=True, on_delete=models.SET_NULL)

class Meta:
        db_table                    = 'client_registration'  
        verbose_name                = 'Client Registration'  
        verbose_name_plural         = 'Client Registrations'  
        ordering                    = ['created_at'] 