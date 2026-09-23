from user.models import User
from django.db import models
from client.models import ClientRegistration

class DashboardConfigurations(models.Model):
    client                          = models.OneToOneField(ClientRegistration, on_delete=models.CASCADE)
    company_id                      = models.PositiveIntegerField(null=True, default=0)
    user_id                         = models.PositiveIntegerField(null=True)
    created_at                      = models.DateTimeField(auto_now_add=True)
    updated_at                      = models.DateTimeField(auto_now=True)
    is_client_dashboard             = models.BooleanField(default=False)
    assign_to                       = models.ForeignKey(User, on_delete=models.PROTECT)
    status                          = models.CharField(max_length=20, default="Not Assigned")
    
    class Meta:
        verbose_name_plural         = "Dashboard Configurations"
        ordering                    = ["-created_at"]  

    def __str__(self):
        return f"Dashboard Config for {self.client}"