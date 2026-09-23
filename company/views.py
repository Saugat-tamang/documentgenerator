from company import service
from django.contrib import messages
from django.http import JsonResponse
from .models import Company, FiscalYear
from client.models import ClientRegistration
from dashboard.models import DashboardConfigurations
from django.db.models.deletion import ProtectedError
from django.views.decorators.csrf import csrf_exempt
from DocumentGenerator.decoder import permission_required_redirect
from django.contrib.auth.decorators import login_required
from user.decorator import admin_required, superuser_required
from django.shortcuts import render, redirect, get_object_or_404
from DocumentGenerator.bulkdelete import check_field_exists, datatable_json_response


# Add Fiscal Year
@login_required
@permission_required_redirect('company.add_fiscalyear', redirect_url='/fiscal/add/')
def fiscal_create(request):
    try:
        data = {
            'title'                     : "Fiscal Year",      
        }
        return render(request,"fiscalyear/form.html",data)
    except:
        return render(request,"error.html")
    
@login_required  
@permission_required_redirect('company.add_fiscalyear', redirect_url='/fiscal/add/')
def fiscal_store(request):
    try:
        store                           = service.storeFiscalYear(request)
        return redirect('fiscal.list')
    except:
        return render(request,"error.html")

@login_required
@permission_required_redirect('company.change_fiscalyear', redirect_url='/fiscal/list/')
def fiscal_edit(request,id):
    try:
        fiscal                          = service.getFiscal(id)
        data = {
            'title'                     : 'Fiscal Year',
            'fiscal'                    : fiscal,  
        }
        return render(request,'fiscalyear/form.html',data)
    except:
        return render(request,"error.html")

@login_required
@permission_required_redirect('company.change_fiscalyear', redirect_url='/fiscal/list/')
def fiscal_update(request,id):
    try:
        service.updateFiscal(request, id)
        return redirect('fiscal.list')
    except:
        return render(request,"error.html")



@login_required
@permission_required_redirect('company.delete_fiscalyear', redirect_url='/fiscal/list/')
def fiscal_delete(request, id):
    try:
        service.deleteFiscal(request, id)
        messages.success(request, "Fiscal Year deleted successfully.")
    except ProtectedError:
        messages.error(request, "This Fiscal Year is currently in use and cannot be deleted.")
    return redirect('fiscal.list')

@login_required
@permission_required_redirect('company.view_fiscalyear', redirect_url='/fiscal/list/')
def fiscal_list(request):
    columns                             = ['id', 'name', 'start_from', 'end_date']
    search_fields                       = ['name', 'start_from', 'end_date']

    extra_context = {
        'template_name'                 : 'fiscalyear/list.html'
    }

    return datatable_json_response(request, model=FiscalYear, columns=columns, search_fields=search_fields,extra_context=extra_context)
    
@superuser_required
def realtime_validation_fisicalyear(request):
    try:
        if request.method == 'GET':
            fiscal_year                 = request.GET.get('start_from', None)
            fiscal_year_id              = request.GET.get('id', None)
            if fiscal_year:
                fiscal_year             = fiscal_year.strip()
                if fiscal_year_id:
                    exists              = FiscalYear.objects.filter(start_from=fiscal_year).exclude(id=fiscal_year_id).exists()
                else:
                    exists              = FiscalYear.objects.filter(start_from=fiscal_year).exists()
                return JsonResponse({'exists': exists})
        return JsonResponse({'exists': False}, status=400)
    except:
        return render(request,"error.html")


@login_required
@permission_required_redirect('company.change_fiscalyear', redirect_url='/fiscal/list/')
def change_fiscalyear(request):
    try:
        fiscal                          = FiscalYear.objects.all()
        data = {
            'title'                     : "Fiscal Year Change",
            'fiscal'                    : fiscal
        }
        return render(request,"fiscalyear/changefisicalyear.html",data)
    except:
        return render(request, 'error.html')
    
 
@login_required
@permission_required_redirect('company.change_fiscalyear', redirect_url='/fiscal/list/')
def change_client_fiscalyear(request):
    try:
        client_id                       = request.session.get('client_id')
        if not client_id:
            return redirect('client_list') 

        client                          = get_object_or_404(ClientRegistration, id=client_id)
        dashboardconfig                 = get_object_or_404(DashboardConfigurations, client__id=client_id)
        fiscal                          = FiscalYear.objects.values('id', 'name')

        data = {
            'title'                     : "Client Fiscal Year Change",
            'client'                    : client,
            'fiscal'                    : fiscal,
            'client_id'                 : client_id,
            'dashboard'                 : dashboardconfig,
            'client_fiscal_year'        : client.fiscal_year
        }
        return render(request, "fiscalyear/client_fiscalyear.html", data)
    except:
        return render(request, "error.html")
        

@login_required
@permission_required_redirect('company.change_fiscalyear', redirect_url='/fiscal/list/')
def update_client_fiscalyear(request):
    if request.method == "POST":
        client_id                       = request.session.get('client_id')
        fiscal_id                       = request.POST.get('fiscal')

        if not client_id or not fiscal_id:
            messages.error(request, "Please select a client and fiscal year.")
            return redirect('change_client_fiscalyear')

        client                          = get_object_or_404(ClientRegistration, id=client_id)
        fiscal                          = get_object_or_404(FiscalYear, id=fiscal_id)
        client.fiscal_year              = fiscal
        client.save()

        messages.success(request, f"Fiscal year changed to {fiscal.name} for this client.")
        return redirect('change_client_fiscalyear')
    return redirect('change_client_fiscalyear')

@login_required
@permission_required_redirect('company.change_fiscalyear', redirect_url='/fiscal/list/')
def update_fiscalyear(request):
    try:
        company                         = Company.objects.get(pk=request.user.company.id)
        new_fiscal                      = FiscalYear.objects.get(pk=request.POST['fiscal'])
        old_fiscal                      = company.fiscal_year  # store old fiscal year
        # Update company fiscal year
        company.fiscal_year             = new_fiscal
        company.save()
        # Update clients who are still using the old company fiscal year
        ClientRegistration.objects.filter(
            company_id=company.id,
            fiscal_year=old_fiscal  # only clients still synced with old fiscal
        ).update(fiscal_year=new_fiscal)

        return redirect('fiscal.changefiscalyear')
    except Exception as e:
        print("Error in update_fiscalyear:", e)
        return render(request, "error.html")


@login_required
@permission_required_redirect('company.view_company', redirect_url='/company/list/')
def company_list(request):
    try:
        if request.user.is_admin:  
            filter_kwargs                   = {}   
        else:
            filter_kwargs = {'id': request.user.company_id}

        columns                             = ['id', 'name', 'address', 'pan', 'province', 'email']
        search_fields                       = ['name', 'address', 'pan', 'province', 'email']

        extra_context = {
            'template_name'                 : 'company/list.html'
        }
        return datatable_json_response(request,filter_kwargs=filter_kwargs, model=Company, columns=columns, search_fields=search_fields, extra_context=extra_context)
    except:
        return render(request,"error.html")


@login_required
@permission_required_redirect('company.add_company', redirect_url='/company/add/')
def company_create(request):
    try:
        fiscal                          = FiscalYear.objects.all()
        data = {
            'title'                     : 'Company Information',
            'fiscal'                    : fiscal,
        }
        return render(request,'company/form.html', data)
    except:
        return render(request,"error.html")
    
    
@login_required
@admin_required
def company_store(request):
    try:
        store                           = service.storeCompany(request)
        return redirect('company.list')
    except:
        return render(request,"error.html")

@login_required
@permission_required_redirect('company.change_company', redirect_url='/company/list/')
def company_edit(request, id):
    try:
        fiscal                          = FiscalYear.objects.all()
        company                         = service.getCompany(id)
        data = {
            'title'                     : 'Company',
            'company'                   : company,
            'fiscal'                    : fiscal,
        }
        return render(request,'company/form.html',data)
    except:
        return render(request,"error.html")
    
@login_required
@permission_required_redirect('company.change_company', redirect_url='/company/list/')
def company_update(request,id):
    try:
        service.updateCompany(request, id)
        return redirect('company.list')
    except:
        return render(request,"error.html")
    
@login_required
@permission_required_redirect('company.delete_company', redirect_url='/company/list/')
def company_delete(request, id):
    try:
        service.deleteCompany(request,id)
        return redirect('company.list')
    except:
        return render(request,"error.html")
    
@login_required
@csrf_exempt
def ajax_loaddata_companyname(request):
    return check_field_exists(request, Company, 'name')

@login_required
@csrf_exempt
def ajax_loaddata_companypan(request):
    return check_field_exists(request, Company, 'pan')