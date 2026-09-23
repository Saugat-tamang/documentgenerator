from django.contrib import admin
from .models import ClientRegistration


@admin.register(ClientRegistration)
class ClientRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'pan', 'client_code', 'email')
    search_fields = ('name', 'pan', 'client_code', 'email')
