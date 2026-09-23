from client import service
import datetime, xlwt, xlrd
from user.models import User
from django.urls import reverse
from django.db import transaction
from company.models import Company
from django.contrib import messages
from client.models import ClientRegistration
from django.http import HttpResponse,JsonResponse
from dashboard.models import DashboardConfigurations
from django.views.decorators.cache import never_cache
from DocumentGenerator.decoder import permission_required_redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404



@login_required
@permission_required_redirect('client.add_clientregistration', redirect_url='/client/client/add/')
def client_create(request): 
    try:
        fiscal                                      = Company.objects.all()
        data = {                    
            'title'                                 : 'New Client Registration Form',
            'fiscal'                                : fiscal,
        }
        return render(request, 'client/form.html', data)
    except:
       return render(request,"error.html")

@login_required
@permission_required_redirect('client.add_clientregistration', redirect_url='/client/client/add/')
def client_create_import(request):
    try:
        data = {
            'title'                                 : 'Client Import Bulk',
        }
        return render(request,"importclient/form.html")
    except:
       return render(request,"error.html",data)


@login_required
@permission_required_redirect('client.view_clientregistration', redirect_url='/client/list/')
def client_list(request):
    return render(request, 'client/list.html')


@login_required
def client_list_json(request):
    try:
        company_id                                  = request.user.company_id
        user_id                                     = request.user.id
        queryset                                    = ClientRegistration.objects.filter(company_id=company_id,user_id=user_id).values('id', 'name', 'address', 'pan', 'email', 'mobile').all()
        clients                                     = list(queryset)
        return JsonResponse({'data': clients})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def client_store(request):
    try:
        if request.method == "POST":
            service.storeClient(request)
            return redirect('client.list')
        return render(request, 'client/form.html')
    except:
        return render(request, "error.html")

@login_required
@permission_required_redirect('client.delete_clientregistration', redirect_url='/client/list/')
def client_delete(request, id):
    try:
        service.deleteClient(request,id)
        return redirect('client.list')
    except:
        return render(request,"error.html")


@never_cache
@login_required
@permission_required_redirect('client.change_clientregistration', redirect_url='/client/list/')
def client_edit(request, id):
    client = ClientRegistration.objects.filter(id=id).first()
    
    if not client:
        messages.error(request, "This client no longer exists.")
        return redirect('client.list')

    data = {
        'title': 'Client',
        'client': client,
    }
    return render(request, 'client/form.html', data)


@login_required
@permission_required_redirect('client.change_clientregistration', redirect_url='/client/list/')
def client_update(request,id):
    try:
        service.updateClient(request, id)
        return redirect('client.list')
    except:
       return render(request,"error.html")
   
@login_required
@permission_required_redirect('client.add_clientregistration', redirect_url='/client/list/')
def export_clients_to_excel(request):
    try:
        model_fields                                = ["name", "address", "pan", "tax_office", "phone", "registration_office", "vat_return_filing_type", "client_code"]
        response                                    = HttpResponse(content_type='application/ms-excel')
        filename                                    = request.POST.get("export_file_name", "client") + "_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.xls'
        response['Content-Disposition']             = f'attachment; filename={filename}'
        workbook                                    = xlwt.Workbook(encoding='utf-8')
        worksheet                                   = workbook.add_sheet("Clients")
        bold_font_style                             = xlwt.XFStyle()
        bold_font_style.font.bold                   = True
        for col_index, field_name in enumerate(model_fields):
            worksheet.write(0, col_index, field_name, bold_font_style)
        rows                                        = ClientRegistration.objects.all()
        for row_index, row in enumerate(rows, start=1):
            for col_index, field_name in enumerate(model_fields):
                value                               = getattr(row, field_name, "") 
                worksheet.write(row_index, col_index, str(value))
        workbook.save(response)
        return response
    except:
        return render(request,"error.html")
    
@login_required
@permission_required_redirect('client.import_clientregistration', redirect_url='/client/list/')
def import_client_excel(request):
    company_id                                      = request.user.company_id
    if request.method != 'POST' or not request.FILES.get('excelbalance'):
        return render(request, 'import_client_excel.html', {'error': 'No file uploaded'})
    
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'error_message': 'User not authenticated'})
    
    try:
        excel_file = request.FILES['excelbalance']
        if not excel_file.name.endswith(('.xls', '.xlsx')):
            return render(request, 'error.html', {'error_message': 'Invalid file format. Please upload an Excel file (.xls or .xlsx)'})
        workbook                                    = xlrd.open_workbook(file_contents=excel_file.read())
        sheet                                       = workbook.sheet_by_index(0)
        field_names = [
            'name', 'address', 'pan', 'tax_office', 'phone',
            'registration_office', 'vat_return_filing_type', 'client_code'
        ]

        default_values = {
            'entity_type'                           : 'Demo Entity',
            'mobile'                                : '0000000000',
            'email'                                 : 'demo@example.com',
            'nature_of_business'                    : 'Demo Business',
            'managing_director'                     : 'John Doe',
            'tax_date_of_registration'              : '2000-01-01',
            'tax_registration_no'                   : '000000',
            'tax_filling_period'                    : 'Monthly',
            'vat_date_of_registration'              : '2000-01-01',
            'vat_registration_no'                   : '000000',
            'vat_filling_period'                    : 'Monthly',
            'company_date_of_registration'          : '2000-01-01',
            'company_registration_no'               : '000000',
            'company_filling_period'                : 'Yearly',
            'gharelu_date_of_registration'          : '2000-01-01',
            'gharelu_registration_no'               : '000000',
            'gharelu_filling_period'                : 'Yearly',
            'service_contract'                      : 'Demo Contract',
            'documents'                             : None,
        }
        rows_data                                   = []
        existing_pans                               = set(ClientRegistration.objects.filter(company_id=company_id).values_list('pan', flat=True))
        duplicate_pans                              = []
        pan_set                                     = set()
        for row_idx in range(1, sheet.nrows):
            row_values                              = sheet.row_values(row_idx)
            data = {
                field: str(row_values[idx]).strip() if idx < len(row_values) else ''
                for idx, field in enumerate(field_names)
            }
            pan_value                               = data.get('pan', '')
            if pan_value:
                try:
                    pan_value                       = str(int(float(pan_value))).zfill(9)
                    if len(pan_value) != 9 or not pan_value.isdigit():
                        return render(request, 'error.html', {
                            'error_message': f"Invalid PAN format '{pan_value}' in row {row_idx + 1}. PAN must be 9 digits."
                        })
                    data['pan']                     = pan_value
                    if pan_value in pan_set:
                        duplicate_pans.append((pan_value, row_idx + 1))
                    pan_set.add(pan_value)
                    if pan_value in existing_pans:
                        duplicate_pans.append((pan_value, row_idx + 1))
                except (ValueError, TypeError):
                    return render(request, 'error.html', {
                        'error_message': f"Invalid PAN format '{pan_value}' in row {row_idx + 1}. PAN must be 9 digits."
                    })

            phone_value = data.get('phone', '')
            if phone_value:
                phone_value                         = ''.join(filter(str.isdigit, phone_value))
                if len(phone_value) < 7 or len(phone_value) > 15:
                    return render(request, 'error.html', {
                        'error_message': f"Invalid phone number '{phone_value}' in row {row_idx + 1}. Phone must be 7-15 digits."
                    })
                data['phone'] = phone_value

            data.update({
                'company_id'                        : request.user.company_id,
                'user_id'                           : request.user.id,
                'fiscal_year'                       : request.user.company.fiscal_year,
                **default_values
            })
            rows_data.append(data)

        if duplicate_pans:
            error_message = 'Duplicate PANs found: ' + ', '.join(
                f"'{pan}' in row {row_num}" for pan, row_num in duplicate_pans
            )
            return render(request, 'error.html', {'error_message': error_message})

        with transaction.atomic():
            for data in rows_data:
                client                              = ClientRegistration.objects.create(**data)
                DashboardConfigurations.objects.create(
                    client                          = client,
                    company_id                      = request.user.company_id,
                    user_id                         = request.user.id,
                    assign_to                       = User.objects.get(id=request.user.id),
                    is_client_dashboard             = True,
                    status                          = 'Not Assigned',
                )
        return redirect('client.list')
    except xlrd.XLRDError:
        return render(request, 'error.html', {'error_message': 'Invalid Excel file format'})
    except User.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'User does not exist'})
    except Exception as e:
        return render(request, 'error.html', {'error_message': f'Error processing file: {str(e)}'})


# =======================
# STEP 1: UPLOAD & VALIDATE
# =======================
@login_required
def import_excel_client(request):
    if request.method == 'POST':
        company_id                                  = request.user.company_id
        file                                        = request.FILES.get('excelbalance')

        if not file:
            return JsonResponse({'success': False, 'error': 'No file uploaded.'})

        try:
            sheet                                   = xlrd.open_workbook(file_contents=file.read()).sheet_by_index(0)
            expected                                = ["name", "address", "pan", "tax_office", "phone", "registration_office", "vat_return_filing_type", "client_code"]
            actual                                  = [str(c.value).strip().lower() for c in sheet.row(0)]

            if actual != expected:
                return JsonResponse({'success': False, 'error': 'Excel header mismatch. Please use the correct template.'})

            data                                    = []
            for i in range(1, sheet.nrows):
                row_number                          = i + 1
                name                                = str(sheet.cell_value(i, 0)).strip()
                address                             = str(sheet.cell_value(i, 1)).strip()
                pan                                 = str(sheet.cell_value(i, 2)).split('.')[0].strip()
                tax_office                          = str(sheet.cell_value(i, 3)).strip()
                phone                               = str(sheet.cell_value(i, 4)).strip()
                registration_office                 = str(sheet.cell_value(i, 5)).strip()
                vat_type                            = str(sheet.cell_value(i, 6)).strip()
                client_code                         = str(sheet.cell_value(i, 7)).strip()

                data.append({
                    'row'                           : row_number,
                    'name'                          : name,
                    'address'                       : address,
                    'pan'                           : pan,
                    'tax_office'                    : tax_office,
                    'phone'                         : phone,
                    'registration_office'           : registration_office,
                    'vat_type'                      : vat_type,
                    'client_code'                   : client_code,
                })

            request.session['preview_client_data']  = data
            return JsonResponse({'success': True, 'redirect_url': reverse('clients.import.preview')})

        except Exception as e:
            return JsonResponse({'success': False, 'error': f"Error reading Excel: {str(e)}"})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


# =======================
# STEP 2: PREVIEW PAGE
# =======================
@login_required
def import_preview_client(request):
    data                                            = request.session.get('preview_client_data', [])
    if not data:
        return redirect('client.list')

    return render(request, 'importclient/import_preview.html', {'data': data,})


# =======================
# STEP 3: SAVE TO DATABASE
# =======================
@login_required
def import_save_client(request):
    if request.method == 'POST':
        company_id                                  = request.user.company_id
        preview_data                                = request.session.get('preview_client_data', [])

        for row in preview_data:
            row_number                              = row['row']
            row['name']                             = request.POST.get(f'name_{row_number}', '').strip()
            row['address']                          = request.POST.get(f'address_{row_number}', '').strip()
            row['pan']                              = request.POST.get(f'pan_{row_number}', '').strip()
            row['tax_office']                       = request.POST.get(f'tax_office_{row_number}', '').strip()
            row['phone']                            = request.POST.get(f'phone_{row_number}', '').strip()
            row['registration_office']              = request.POST.get(f'registration_office_{row_number}', '').strip()
            row['vat_type']                         = request.POST.get(f'vat_type_{row_number}', '').strip()
            row['client_code']                      = request.POST.get(f'client_code_{row_number}', '').strip()
            row['errors']                           = {}

        seen_names                                  = set()
        seen_pans                                   = set()
        seen_client_no                              = set()
        valid_rows                                  = []

        for row in preview_data:
            name                                    = row['name']
            pan                                     = row['pan']
            client_code                             = row['client_code']
            phone                                   = row['phone']

            if not name:
                row['errors']['name']               = "Name is required"
            elif name in seen_names or ClientRegistration.objects.filter(name=name, company_id=company_id).exists():
                row['errors']['name']               = "Name already exists in this company"
            else:
                seen_names.add(name)

            if not client_code:
                row['errors']['client_code']        = "Client Code is required"
            elif client_code in seen_client_no or ClientRegistration.objects.filter(client_code=client_code, company_id=company_id).exists():
                row['errors']['client_code']        = "Client code already exists in this company"
            else:
                seen_client_no.add(client_code)

            if pan:
                if not pan.isdigit() or len(pan) != 9:
                    row['errors']['pan']            = "PAN must be 9 digits"
                elif pan in seen_pans or ClientRegistration.objects.filter(pan=pan, company_id=company_id).exists():
                    row['errors']['pan']            = "Pan already exists in this company"
                else:
                    seen_pans.add(pan)

            if phone:
                if not phone.isdigit() or len(phone) != 10:
                    row['errors']['phone']          = "Phone must be 10 digits"

            if not row['errors']:
                valid_rows.append(row)

        fiscal_year                                 = request.user.company.fiscal_year
        
        with transaction.atomic():
            for row in valid_rows:
                client                              = ClientRegistration.objects.create(
                    name                            = row['name'],
                    address                         = row['address'],
                    pan                             = row['pan'],
                    phone                           = row['phone'],
                    registration_office             = row['registration_office'],
                    vat_return_filing_type          = row['vat_type'],
                    client_code                     = row['client_code'],
                    company_id                      = company_id,
                    documents                       = None,
                    user_id                         = request.user.id,
                    fiscal_year                     = fiscal_year,
                )

                DashboardConfigurations.objects.create(
                    client                          = client,
                    company_id                      = request.user.company_id,
                    user_id                         = request.user.id,
                    assign_to                       = User.objects.get(id=request.user.id),
                    is_client_dashboard             = True,
                    status                          = 'Not Assigned',
                )

        request.session['preview_client_data']      = [row for row in preview_data if row['errors']]

        if request.session['preview_client_data']:
            return redirect('clients.import.preview')

        request.session.pop('preview_client_data', None)
        return redirect('client.list')

    return redirect('client.list')


def client_details(request, client_id):
    try:
        client_id                                   = request.session.get('client_id')
        if client_id is None:
            return render(request, 'error.html', {'message': 'Client ID not found in session.'})
        client_registration                         = get_object_or_404(ClientRegistration, id=client_id)
        dashboard_config                            = DashboardConfigurations.objects.get(client__id=client_id)
        return render(request, 'client/details.html', {
            'dashboard'                             : dashboard_config,
            'client_registration'                   : client_registration,
            'client_id'                             : client_id                                      
        }) 
    except:
        return render(request,"error.html")
    
def client_vat_status_change(request):
    client_id                                       = request.session.get('client_id')
    if not client_id:
        return redirect("client_dashboard")

    client                                          = get_object_or_404(ClientRegistration, pk=client_id)
    dashboard_config                                = get_object_or_404(DashboardConfigurations, client__id=client_id)

    if request.method == "POST":
        vat_type                                    = request.POST.get("vat_return_filing_type")
        if vat_type:
            client.vat_return_filing_type = vat_type
            client.save()
            messages.success(request, "Client status updated successfully!")
            return redirect("client.status.change") 
        else:
            messages.error(request, "Please select a VAT return filing type.")

    data = {
        "client"                                    : client,           
        "client_id"                                 : client_id,
        "dashboard"                                 : dashboard_config,
        "title"                                     : "Update Client VAT Filing Type"
    }
    return render(request, 'client/statuschange.html', data)