from auditlog.models import AuditLog
from DocumentGenerator.helper import nep_to_eng_date_con

def getAllAuditlog(request):
    return AuditLog.objects.filter(company_id = request.user.company_id).all()

def auditlogList(request):
    dateRange                           = [nep_to_eng_date_con(str(request.POST["startdate"])), nep_to_eng_date_con(str(request.POST["enddate"]))]
    user                                = request.POST['user']
    auditlog                            = AuditLog.objects.filter(updated_at__range=dateRange,user_id=user,company_id = request.user.company_id)
    return auditlog

def saveAuditLogs(module, action,model, request):
    auditLog                            = AuditLog(
        module                          = module,
        action                          = action,
        model                           = model,
        company_id                      = request.user.company_id, 
        user                            = request.user,
        user_email                      = request.user.email,
        user_name                       = request.user.username,
    )
    auditLog.save()
    return auditLog