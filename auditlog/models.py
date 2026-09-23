from django.db import models
from client.models import ClientRegistration
from company.models import FiscalYear
from user.models import User

class AuditLog(models.Model):
    module                                = models.CharField(max_length=100, default=None, null=True)
    action                                = models.CharField(max_length=100, null=True)
    user                                  = models.ForeignKey(User, on_delete=models.PROTECT)
    user_email                            = models.EmailField()
    user_name                             = models.CharField(max_length=100,null=True)
    model                                 = models.CharField(max_length=100,null=True)

    company_id                            = models.PositiveIntegerField(null=True,default=0)
    created_at                            = models.DateTimeField(auto_now_add=True)
    updated_at                            = models.DateTimeField(auto_now=True)

    class Meta:
          verbose_name                    = "Audit Log"
          verbose_name_plural             = "Audit Logs"
          ordering                        = ['-created_at']
          indexes = [
              models.Index(fields         = ['module']),
              models.Index(fields         = ['action']), 
              models.Index(fields         = ['user']),
         ]

    @property 
    def formatted_nepalidate(self):
         return self.updated_at.strftime("%Y-%m-%d %H:%M:%S") 
    
    def __str__(self):
         return f"AuditLog {self.module} - {self.action}"