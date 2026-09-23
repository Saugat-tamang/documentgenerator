from user.models import User
from company.models import FiscalYear
from .models import ClientRegistration
from auditlog.service import saveAuditLogs
from django.shortcuts import get_object_or_404
from dashboard.models import DashboardConfigurations

def getClientList():
    client                                      = ClientRegistration.objects.values().all()
    return list(client)

def storeClient(request):
    company_fiscal_year                         = request.user.company.fiscal_year
    fiscal_year_id                              = request.POST.get('fiscal_year')
    if fiscal_year_id:
        fiscal_year                             = get_object_or_404(FiscalYear, pk=fiscal_year_id)
    else:
        fiscal_year = company_fiscal_year
    client_generate                             = ClientRegistration(
        name                                    = request.POST.get('name'),
        pan                                     = request.POST.get('pan'),
        client_code                             = request.POST.get('client_code'),
        phone                                   = request.POST.get('phone'),
        email                                   = request.POST.get('email'),
        company_id                              = request.user.company_id,
        user_id                                 = request.user.id,
        address                                 = request.POST.get('address'),
        logo                                    = request.FILES.get('logo'),
        sign                                    = request.FILES.get('sign'),
        stamp                                   = request.FILES.get('stamp'),
        fiscal_year                             = company_fiscal_year
    )
    client_generate.save()
    dashboard                                   = DashboardConfigurations(
        client                                  = ClientRegistration.objects.get(pk=client_generate.id),        
        company_id                              = request.user.company_id,       
        user_id                                 = request.user.id, 
        assign_to                               = User.objects.get(id=request.user.id),
        is_client_dashboard                     = True,
        status                                  = 'Not Assigned',    
    )
    dashboard.save()
    saveAuditLogs("ClientRegistration", "Save", "ClientRegistration", request)
   
def getClient(id):
    client                                      = ClientRegistration.objects.get(id= id)
    return client

def deleteClient(request,id):
    client                                      = ClientRegistration.objects.get(id = id)
    client.delete()
    saveAuditLogs("ClientRegistration", "Deleted", "ClientRegistration", request)

def updateClient(request, id):
    client                                      = ClientRegistration.objects.get(id=id)
    client.name                                 = request.POST.get('name')
    client.pan                                  = request.POST.get('pan')
    client.client_code                          = request.POST.get('client_code')
    client.email                                = request.POST.get('email')
    client.address                              = request.POST.get('address')
    client.phone                                = request.POST.get('phone')
    client.stamp                                = request.FILES.get('stamp'),

    if request.FILES.get('logo'):
        client.logo                        = request.FILES.get('logo')

    if request.FILES.get('sign'):
        client.sign                        = request.FILES.get('sign')

    if request.FILES.get('stamp'):
        client.stamp                        = request.FILES.get('stamp')

    client.save()
    saveAuditLogs("ClientRegistration", "Updated", "ClientRegistration", request)