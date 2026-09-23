from .models import *
from auditlog.service import saveAuditLogs
from django.contrib.auth import authenticate

def authenticateuser(email,password):
    return authenticate(email=email, password=password)

def storeUser(request,company,company_admin,is_superuser,is_employee,role=None):
    user = User(
      email                         = request.POST['email'],
      username                      = request.POST['username'],
      is_staff                      = True,
      is_admin                      = False,
      is_superuser                  = is_superuser,
      company                       = company,
      company_admin                 = company_admin,
      is_employee                   = is_employee,
      english_fullname              = request.POST.get('english_fullname',None),
      profile_image                 = request.FILES.get('profile_images'),
    )
    user.set_password(request.POST['password'])
    user.save()
    if role:
        user.groups.add(role)
    saveAuditLogs("User", "Save", "User", request)


def getUser(id):
    return User.objects.get(id = id)

def getUserList():
    user                             = User.objects.values().all()
    return list(user)

def deleteUser(request,id):
    user                             = User.objects.get(id=id)
    user.delete()
    saveAuditLogs("User", "deleted",'User', request)
    
    
def updateUserProfile(request,id):
    user                              = User.objects.get(pk=id)
    user.english_fullname             = request.POST['english_fullname']
    user.save()
 
 
def getUserProfileDetails(id):
    return User.objects.filter(pk=id).get()
  