import base64, json
from user.models import User
from django.db.models import Q
from django.http import JsonResponse
from .models import DashboardConfigurations
from client.models import ClientRegistration
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from DocumentGenerator.decoder import permission_required_redirect

@login_required
def index(request):
        request.session.pop('client_id', None)
        company_id                          = request.user.company_id
        client                              = ClientRegistration.objects.filter(company_id=company_id).order_by('-created_at').all()[:5]
        length_of_client                    = len(client)
        dashboard_data                      = DashboardConfigurations.objects.none()
        dashboard_data_index                = DashboardConfigurations.objects.filter(company_id=company_id)
        if hasattr(request.user, 'is_employee') and request.user.is_employee:
            dashboard_data                  = DashboardConfigurations.objects.filter(assign_to_id=request.user.id).order_by('id')

        data = {
            'client'                        : client,
            'length_of_client'              : length_of_client,
            'dashboard_data'                : dashboard_data,
            'dashboard_data_index'          : dashboard_data_index
        }
        return render(request, 'dashboard/index.html', data)
    
    
@login_required
@permission_required_redirect('client.view_clientregistration', redirect_url='/home/')
def index_list(request):
    try:
        return render(request, 'dashboard/list.html')
    except:
        return render(request,"error.html")


@login_required
def client_dashboard(request, client_id):
    user = request.user

    try:
        # ======================================================
        # Dashboard Configuration
        # ======================================================
        if user.is_superuser or user.is_admin:
            dashboard_config = get_object_or_404(
                DashboardConfigurations,
                client__id=client_id,
            )
        else:
            dashboard_config = get_object_or_404(
                DashboardConfigurations,
                client__id=client_id,
                assign_to=user,
            )

        # Session client
        request.session['client_id'] = client_id
        fiscal_year = dashboard_config.client.fiscal_year

        return render(
            request,
            'dashboard/index1.html',
            {
                'dashboard': dashboard_config,
                'client_id': client_id,
            },
        )

    except Exception as e:
        print("Error in client_dashboard:", e)
        return redirect('/home/')

    
@login_required
def exit_client_dashboard(request):
    # Clear client context so client-specific menus/widgets (e.g., TDS)
    # do not appear on the main dashboard.
    request.session.pop('client_id', None)
    return redirect('index') 




@login_required
def assign_client_to_user(request):
    try:
        company_id                          = request.user.company_id
        disabled_clients                    = list(DashboardConfigurations.objects.filter(company_id=company_id,status="Assigned").values_list("client_id", flat=True).distinct())
        user_data                           = User.objects.filter(company_id=company_id,is_employee=True).all()
        client                              = ClientRegistration.objects.filter(company_id=company_id).all()
        data = {
            'user_data'                     : user_data,
            'client'                        : client,
            'disabled_client'               : disabled_clients
        }
        return render(request,'assign/form.html',data)
    except:
        return render(request,"error.html")

def update_dashboard(request):
    try:
        if request.method == "POST":
            company_id                      = request.user.company_id
            client_ids                      = request.POST.getlist("select_client")
            assign_to_id                    = request.POST.get("assign_to")
            client_ids                      = [int(client_id) for client_id in client_ids] 
            assign_to                       = get_object_or_404(User, id=int(assign_to_id))
            user_assigned_count             = DashboardConfigurations.objects.filter(company_id=company_id,assign_to=assign_to,status="Assigned").count()

            total_after_assignment          = user_assigned_count + len(client_ids)

            if total_after_assignment > 3:
                return redirect('client.list')
            updated_count                   = DashboardConfigurations.objects.filter(company_id=company_id,client_id__in=client_ids).update(assign_to=assign_to,status="Assigned")
        return redirect('client.list')
    except:
        return render(request,"error.html")
    
    
@login_required
def dashboard_config_list(request):
    return render(request, 'assign/list.html')


@login_required
def dashboard_config_data(request):
    company_id                              = request.user.company_id
    configs                                 = DashboardConfigurations.objects.select_related("client", "assign_to").order_by("id").filter(company_id=company_id)
    
    users                                   = User.objects.filter(company_id=company_id)
    
    data                                    = []
    for idx, config in enumerate(configs, start=1):
        user_options = "".join(
            f"<option value='{user.id}' {'selected' if config.assign_to and config.assign_to.id == user.id else ''}>{user.username}</option>"
            for user in users
        )
        data.append([
            idx,
            config.client.name,
            f"<select class='form-select assign-to-dropdown' data-id='{config.id}'>{user_options}</select>",
            f"<select class='form-select status-dropdown' data-id='{config.id}'>"
            f"<option value='Assigned' {'selected' if config.status == 'Assigned' else ''}>Assigned</option>"
            f"<option value='Not Assigned' {'selected' if config.status == 'Not Assigned' else ''}>Un Assigned</option>"
            "</select>",
            "<span class='badge bg-success'>Yes</span>" if config.is_client_dashboard else "<span class='badge bg-secondary'>No</span>",
        ])
    return JsonResponse({
        "data": data
    })
    
    
@csrf_exempt
def update_dashboard_config(request):
    company_id                              = request.user.company_id
    if request.method == 'POST':
        data                                = json.loads(request.body)
        config_id                           = data.get('id')
        status                              = data.get('status')
        assign_to                           = data.get('assign_to')

        try:
            config                          = DashboardConfigurations.objects.get(id=config_id)
            if status:
                config.status               = status
            if assign_to:
                config.assign_to_id         = assign_to
            config.save()
            return JsonResponse({"success": True})
        except DashboardConfigurations.DoesNotExist:
            return JsonResponse({"success": False, "error": "Not found"})
    return JsonResponse({"success": False, "error": "Invalid method"})


# wrong rul redirect

def custom_404_view(request, exception):
    return redirect('/')



def encode_cursor(last_id: int | None):
    if last_id is None:
        return None
    return base64.urlsafe_b64encode(json.dumps({"last_id": last_id}).encode()).decode()

def decode_cursor(cursor: str | None):
    if not cursor:
        return None
    try:
        data                                = json.loads(base64.urlsafe_b64decode(cursor.encode()).decode())
        return int(data.get("last_id"))
    except:
        return None

@require_GET
def api_clients(request):
    PAGE_SIZE                               = 20
    company_id                              = request.user.company_id
    cursor                                  = decode_cursor(request.GET.get("cursor"))
    q                                       = (request.GET.get("q") or "").strip().lower()

    if request.user.is_employee:
        qs                                  = DashboardConfigurations.objects.filter(company_id=company_id,assign_to_id=request.user.id)
    else:
        qs                                  = DashboardConfigurations.objects.filter(company_id=company_id)

    # Keyset pagination
    if cursor:
        qs                                  = qs.filter(id__gt=cursor)

    # Search filter
    if q:
        qs                                  = qs.filter(
                                                Q(client__name__icontains=q) |
                                                Q(assign_to__username__icontains=q) |
                                                Q(client__address__icontains=q)
                                            )

    qs                                      = qs.select_related("client", "assign_to").only("id","client__id", "client__name", "client__address", "client__vat_return_filing_type","assign_to__username").order_by("id")[:PAGE_SIZE]

    items                                   = []
    last_id                                 = None
    for d in qs:
        last_id                             = d.id
        items.append({
            "id"                            : d.id,
            "name"                          : d.client.name,
            "username"                      : d.assign_to.username,
            "address"                       : d.client.address or "",
            "filing_type"                   : d.client.vat_return_filing_type or "",
            "link"                          : f"/client-dashboard/{d.client.id}/",
            "assign_link"                   : "/assignclienttouser/"
        })

    return JsonResponse({
        "items"                             : items,
        "next_cursor"                       : encode_cursor(last_id) if items else None
    })