from user.models import User
from user.service import storeUser
from .models import FiscalYear, Company
from auditlog.service import saveAuditLogs
from django.shortcuts import get_object_or_404
from DocumentGenerator.healperService import endDateFiscaYear, fiscal_year

# FiscalYear Services
def storeFiscalYear(request):
    start_from                              = request.POST['start_from']
    end_date                                = endDateFiscaYear(start_from)
    name                                    = fiscal_year(start_from)
    fiscal                                  = FiscalYear(
      name                                  = name,
      start_from                            = start_from,
      end_date                              = end_date,
    )
    fiscal.save()
    saveAuditLogs("Fiscal", "Save",'Fiscal', request)

def getFiscal(id):
    fiscal                                  = FiscalYear.objects.get(id = id)
    return fiscal

def updateFiscal(request,id):
    start_from                              = request.POST['start_from']
    end_date                                = request.POST['end_date']
    name                                    = fiscal_year(start_from)
    fiscal                                  = FiscalYear.objects.get(id=id)
    fiscal.start_from                       = start_from
    fiscal.end_date                         = end_date
    fiscal.name                             = name
    fiscal.save()
    saveAuditLogs("Fiscal", "Update",'Fiscal', request)

def deleteFiscal(request, id):
    fiscal = FiscalYear.objects.get(id=id)
    fiscal.delete()  
    saveAuditLogs("Fiscal", "deleted",'Fiscal', request)

# COMPANY LOGIC
def storeCompany(request):
    fiscal_year_id                          = request.POST.get('fiscal_year')
    name                                    = request.POST.get('name')
    fiscal_year                             = get_object_or_404(FiscalYear, id=fiscal_year_id)
    company                                 = Company.objects.create(
        fiscal_year                         = fiscal_year,
        name                                = name,
        print_name                          = request.POST.get('print_name'),
        fiscal_year_beginning_from          = request.POST.get('fiscal_year_beginning_from'),
        book_commencing_from                = request.POST.get('book_commencing_from'),
        address                             = request.POST.get('address'),
        pan                                 = request.POST.get('pan'),
        phone                               = request.POST.get('phone'),
        email                               = request.POST.get('email'),
        image                               = request.FILES.get("image",None),
    )
    company.save()
    storeUser(request,company,True,True,False)
    saveAuditLogs("Company", "Save", "Company", request)

def getCompany(id):
    return Company.objects.get(id = id)

def getCompanyList():
    company                                 = Company.objects.values().all()
    return list(company)

def deleteCompany(request,id):
    company                                 = Company.objects.get(id = id)
    User.objects.filter(company=company).delete()
    company.delete()
    saveAuditLogs("Company", "deleted",'Company', request)

def updateCompany(request, id):
    company                                 = get_object_or_404(Company, id=id)
    company.name                            = request.POST.get('name')
    company.print_name                      = request.POST.get('print_name')
    company.fiscal_year_beginning_from      = request.POST.get('fiscal_year_beginning_from')
    company.book_commencing_from            = request.POST.get('book_commencing_from')
    company.address                         = request.POST.get('address')
    company.pan                             = request.POST.get('pan')
    company.phone                           = request.POST.get('phone')
    company.email                           = request.POST.get('email')
    
    if 'image' in request.FILES:
        company.image                       = request.FILES.get('image')
    company.save()
    saveAuditLogs("Company", "Updated", "Company", request)
# END COMPANY 