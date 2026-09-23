from . import service
from django.urls import *
from user.models import User
from django.shortcuts import render
from DocumentGenerator.decoder import permission_required_redirect
from django.contrib.auth.decorators import login_required

@login_required
@permission_required_redirect('auditlog.add_logentry', redirect_url='/auditlog/credit/')
def auditlogCreate(request):
    try:
        auditlog                                    = service.getAllAuditlog(request)
        user                                        = User.objects.filter(company_id = request.user.company_id).all()
        data = {
            'auditlog'                              : auditlog,
            'user_filter_audit_logs'                : user,
        }
        return render(request, 'auditlog/form.html', data)
    except:
        return render(request, "error.html")
    
@login_required
@permission_required_redirect('auditlog.view_logentry', redirect_url='/auditlog/credit/list/')
def auditlogList(request):
    try:
        listAudit                                   = service.auditlogList(request)
        data = {
            'listAudit'                             : listAudit
        }
        return render(request, 'auditlog/list.html', data) 
    except:
        return render(request, "error.html")