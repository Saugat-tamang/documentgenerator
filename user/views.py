import random
from user import service
from user.models import User
from datetime import timedelta
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import ProtectedError
from user.decorator import superuser_required
from user.utils import validate_user_password
from collections import defaultdict, OrderedDict
from django.contrib.auth import login, get_user_model
from DocumentGenerator.decoder import permission_required_redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from DocumentGenerator.bulkdelete import check_field_exists, datatable_json_response


@csrf_exempt
def user_login_form(request):
    try:
        context                         = {}
        if request.user.is_authenticated:
            return redirect("/home/")
        else:
            return render(request,'user/login.html',context)
    except:
        return render(request,"error.html")


@login_required
@superuser_required
def add_user(request):
    try:
        roles = Group.objects.exclude(name='Admin')
        data = {
            'title'                     : 'user',
            'roles': roles,
        }
        return render(request,'user/form.html',data)
    except:
        return render(request,"error.html") 

@login_required
def store_user(request):
    try:
        password                        = request.POST.get('password')
        password_confirmation           = request.POST.get('password_confirmation')
        role_id                         = request.POST.get('role')
        
        try:
            role = Group.objects.get(id=role_id)
        except Group.DoesNotExist:
            return HttpResponseBadRequest("Role not found.")
        
        if password != password_confirmation:
            messages.error(request, "Passwords do not match.")
            return redirect('user.create')
        password_errors                 = validate_user_password(password)
        if password_errors:
            for error in password_errors:
                messages.error(request, error)
            return redirect('user.create')
        service.storeUser(request, request.user.company, False, False, True, role=role)
        return redirect("user:user.list")
    except:
       return render(request,"error.html")
   
   
    
@login_required
@superuser_required
def user_list(request):
    company_id                          = request.user.company_id
    filter_kwargs                       = {'company_id': company_id}
    
    columns                             = ['id', 'username', 'english_fullname', 'is_staff', 'is_admin', 'is_employee']
    search_fields                       = ['username']

    extra_context = {
        'template_name'                 : 'user/list.html',
        'title'                         : 'User'
    }

    return datatable_json_response(request, model=User, columns=columns,filter_kwargs=filter_kwargs, search_fields=search_fields, extra_context=extra_context)

   
@login_required
def reset_password(request):
    try:
        data = {
        }
        if request.method == 'POST':
            old_password                = request.POST.get('old_password')
            new_password                = request.POST.get('new_password')
            confirm_password            = request.POST.get('confirm_password')
            if new_password == confirm_password:
                if not request.user.check_password(old_password):
                    return render(request, 'user/reset_password.html', {'error': 'old password does not match.',})
                else:
                    request.user.reset_password(old_password, new_password)
                    return redirect('logout')
            else:
                return render(request, 'user/reset_password.html', {'error': 'New passwords do not match.',})
        else:
            return render(request, 'user/reset_password.html',data)
    except:
        return render(request,"error.html")
    
@login_required
@superuser_required
def User_edit(request, id):
    try:
        user                      = service.getUser(id)
        data = {
            'title'               : 'User',
            'user'                :  user, 
        }
        return render(request,'user/form.html',data)
    except:
        return render(request,"error.html")
    
@login_required
@superuser_required
def user_update(request,id):
    try:
        service.updateUserProfile(request, id)
        return redirect('user.list')
    except:
        return render(request,"error.html")
    
@login_required
@superuser_required
def user_delete(request, id):
    try:
        service.deleteUser(request,id)
        return redirect('user:user.list')
    except ProtectedError:
        return render(request, "user/list.html", {"error_message": "This user cannot be deleted because they are assigned to dashboard configurations."})

    
@login_required
def userDetails(request):
    try:
        data = {
            'user':User.objects.get(id=request.user.id),
        }
        return render(request, 'user/details.html', data)
    except:
        return render(request,"error.html")
    
@login_required
def userEdit(request,id):
    try:
        data = {
            'user'                  : User.objects.get(id=request.user.id),
        }
        return render(request, 'user/editdetails.html', data)
    except:
        return render(request,"error.html")


@csrf_exempt
def userprofile_edit(request,id):
    try:
        userprofile = service.getUserProfileDetails(id=id)
        data = {
            'user'               : userprofile,   
        }
        return render(request,'user/editdetails.html',data)
    except:
        return render(request,"error.html")


@csrf_exempt
def userprofile_update(request,id):
    try:
        userprofile                 = service.updateUserProfile(request,id)
        return redirect('user:user.details')
    except:
        return render(request, "error.html")
    

@csrf_exempt
def upload_file(request):
    try:
        if request.method == 'POST':
            profile_image           = request.FILES.get('file1')
            user_id                 = request.POST['userid']
            user                    = get_object_or_404(User, id=user_id)
            user.profile_image      = profile_image
            user.save()
            image_url               = user.profile_image.url if user.profile_image else None
            if profile_image:
                return JsonResponse({'message': 'hello','file_url': image_url})
            return JsonResponse({'message': 'No file uploaded'}, status=400)
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    except:
        return render(request,"error.html")


def generate_otp():
    return str(random.randint(100000, 999999))


@csrf_protect
def auth_user(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            device_id = request.POST.get("device_id")

            authenticated_user = service.authenticateuser(email, password)

            if authenticated_user is not None:
                if not authenticated_user.device_id:
                    authenticated_user.device_id = device_id
                    authenticated_user.save()
                    login(request, authenticated_user)
                    return JsonResponse({"success": True, "redirect_url": "/home/"}) \
                        if request.headers.get("X-Requested-With") == "XMLHttpRequest" \
                        else redirect("/home/")

                if authenticated_user.device_id == device_id:
                    login(request, authenticated_user)
                    return JsonResponse({"success": True, "redirect_url": "/home/"}) \
                        if request.headers.get("X-Requested-With") == "XMLHttpRequest" \
                        else redirect("/home/")

                if authenticated_user.device_id != device_id:
  
                    if authenticated_user.otp_code and authenticated_user.otp_created_at:
                        elapsed = timezone.now() - authenticated_user.otp_created_at
                        if elapsed < timedelta(minutes=5):
                            return JsonResponse({
                                "otp_required": True,
                                "email": email,
                                "device_id": device_id
                            }) if request.headers.get("X-Requested-With") == "XMLHttpRequest" \
                                else redirect(f"/verify-otp-page/?email={email}&device_id={device_id}")

                    # Generate OTP
                    otp = generate_otp()
                    authenticated_user.otp_code = otp
                    authenticated_user.otp_created_at = timezone.now()
                    authenticated_user.save(update_fields=["otp_code", "otp_created_at"])

                    send_mail(
                        subject="New Device Login OTP",
                        message=f"OTP for user {authenticated_user.email} is: {otp}",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[settings.ADMIN_EMAIL],
                        fail_silently=False,
                    )

                    return JsonResponse({
                        "otp_required": True,
                        "email": email,
                        "device_id": device_id
                    }) if request.headers.get("X-Requested-With") == "XMLHttpRequest" \
                        else redirect(f"/verify-otp-page/?email={email}&device_id={device_id}")

            return JsonResponse({"success": False, "error_message": "Invalid credentials"}, status=400) \
                if request.headers.get("X-Requested-With") == "XMLHttpRequest" \
                else render(request, "user/login.html", {"error_message": "Invalid credentials"})

        return redirect("/login/")
    except Exception as e:
        return JsonResponse({"success": False, "error_message": str(e)}, status=500) \
            if request.headers.get("X-Requested-With") == "XMLHttpRequest" \
            else render(request, "user/login.html", {"error_message": str(e)})



@csrf_protect
def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = request.POST.get("otp")
        device_id = request.POST.get("device_id")

        try:
            user = User.objects.get(email=email)

            if user.otp_code == otp and timezone.now() - user.otp_created_at < timedelta(minutes=5):
                if not user.device_id:
                    user.device_id = device_id

                user.otp_code = None
                user.otp_created_at = None
                user.save()

                login(request, user)
                return redirect("/home/")

            return render(request, "user/enter_otp.html", {
                "email": email,
                "device_id": device_id,
                "message": "Invalid or expired OTP. Try again."
            })

        except User.DoesNotExist:
            return render(request, "error.html", {"error_message": "User not found."})
    return render(request, "error.html", {"error_message": "Invalid request."})


def enter_otp_page(request):
    email = request.GET.get("email")
    device_id = request.GET.get("device_id")
    return render(request, "user/enter_otp.html", {
        "email": email,
        "device_id": device_id
    })


@csrf_protect
def forgot_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Generate OTP
            otp = generate_otp()
            user.otp_code = otp
            user.otp_created_at = timezone.now()
            user.save()

            send_mail(
                subject="Forgot Password OTP",
                message=f"Your OTP for resetting password is: {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Email not found'}, status=400)
    return JsonResponse({'success': False, 'error_message': 'Invalid request'}, status=400)


@csrf_protect
def verify_forgot_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')

        if not email or not otp:
            return JsonResponse({'success': False, 'error_message': 'Email or OTP missing'}, status=400)

        try:
            user = User.objects.get(email=email)

            if user.otp_code == otp and timezone.now() - user.otp_created_at < timedelta(minutes=5):
                # Clear OTP
                user.otp_code = None
                user.otp_created_at = None
                user.save()
                request.session['reset_email'] = email
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('user:forgot_password.reset')
                })
            return JsonResponse({'success': False, 'error_message': 'Invalid or expired OTP'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'User not found'}, status=400)
    return JsonResponse({'success': False, 'error_message': 'Invalid request'}, status=400)



@csrf_protect
def resend_forgot_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'success': False, 'error_message': 'Email missing'}, status=400)
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            user.otp_code = otp
            user.otp_created_at = timezone.now()
            user.save()

            send_mail(
                "Password Reset OTP",
                f"Your OTP is: {otp}. It will expire in 5 minutes.",
                "noreply@example.com",
                [email],
                fail_silently=False,
            )
            return JsonResponse({'success': True, 'message': 'OTP resent successfully'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'User not found'}, status=400)
    return JsonResponse({'success': False, 'error_message': 'Invalid request'}, status=400)



@csrf_protect
def reset_password_form(request):
    email = request.session.get('reset_email')
    if not email:
        return JsonResponse({'success': False, 'error_message': 'Session expired. Please login again.'}, status=400)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not new_password or not confirm_password:
            return JsonResponse({'success': False, 'error_message': 'Password fields cannot be empty'}, status=400)

        if new_password != confirm_password:
            return JsonResponse({'success': False, 'error_message': 'Passwords do not match'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'User not found'}, status=400)

        if user.check_password(new_password):
            return JsonResponse({'success': False, 'error_message': 'New password cannot be the same as the old password'}, status=400)

        if email.lower() in new_password.lower():
            return JsonResponse({'success': False, 'error_message': 'New password cannot contain your email'}, status=400)

        password_errors = validate_user_password(new_password)
        if password_errors:
            return JsonResponse({'success': False, 'error_message': password_errors}, status=400)

        # Save new password
        user.set_password(new_password)
        user.save()
        del request.session['reset_email']
        return JsonResponse({'success': True, 'redirect_url': reverse('user:login')})
    return JsonResponse({'success': False, 'error_message': 'Invalid request'}, status=400)



# ============================================
# ROLES AND PERMISSION ROLE BASED PERMISSION 
# ============================================
def is_admin(user):
    return user.is_superuser
from .audit import log_role_assignment

@login_required
@permission_required_redirect('user.add_roles', redirect_url='/home/')
def role_list_view(request):
    roles = Group.objects.exclude(name='admin')
    return render(request, "rbac/list.html", {"roles": roles})

@login_required
@permission_required_redirect('user.add_roles', redirect_url='/home/')
def create_role_view(request):
    if request.method == "POST":
        role_name = request.POST.get("role_name")
        if role_name and not Group.objects.filter(name=role_name).exists():
            Group.objects.create(name=role_name)
            messages.success(request, "Role created.")
        else:
            messages.error(request, "Invalid or duplicate role name.")
        return redirect("user:rolelist")
    return render(request, "rbac/index.html")


@login_required
@permission_required_redirect('user.add_roles', redirect_url='/home/')
def assign_permissions_view(request, role_id):
    role = get_object_or_404(Group, id=role_id)

    grouped_permissions = defaultdict(lambda: OrderedDict([
        ("view", None),
        ("add", None),
        ("change", None),
        ("delete", None)
    ]))

    all_permissions = Permission.objects.all().order_by('content_type__model', 'codename')

    for perm in all_permissions:
        model_name = perm.content_type.model
        codename = perm.codename
        if codename.startswith("view_"):
            grouped_permissions[model_name]["view"] = perm
        elif codename.startswith("add_"):
            grouped_permissions[model_name]["add"] = perm
        elif codename.startswith("change_"):
            grouped_permissions[model_name]["change"] = perm
        elif codename.startswith("delete_"):
            grouped_permissions[model_name]["delete"] = perm
            
                
        if request.method == "POST":
            perms = [int(p) for p in request.POST.getlist("permissions") if p.isdigit()]
            role.permissions.set(Permission.objects.filter(id__in=perms))
            messages.success(request, f"Permissions for '{role.name}' updated successfully.")
            return redirect("user:rolelist")


    return render(request, "rbac/assign_permissions.html", {
        "role": role,
        "permissions": dict(grouped_permissions),  
        "assigned": set(role.permissions.values_list("id", flat=True))
    })



@login_required
@permission_required_redirect('user.add_roles', redirect_url='/home/')
def assign_users_view(request, role_id):
    role = get_object_or_404(Group, id=role_id)
    User = get_user_model()
    users = User.objects.all()

    if request.method == "POST":
        user_ids = request.POST.getlist("users")  

        # Clear all users from the role before reassigning
        role.user_set.clear()

        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                user.groups.add(role)
                # Optional: your logging function, handle exceptions if any
                try:
                    log_role_assignment(user, role)
                except Exception as e:
                    print(f"Logging failed: {e}")
            except User.DoesNotExist:
                continue  

        messages.success(request, "Users assigned to role successfully.")
        return redirect("user:rolelist")

    assigned_ids = role.user_set.values_list("id", flat=True)

    return render(request, "rbac/assign_users.html", {
        "role": role,
        "users": users,
        "assigned_ids": assigned_ids,
    })



@login_required
@permission_required_redirect('user.add_roles', redirect_url='/home/')
def role_users_permissions_view(request):
    groups = Group.objects.exclude(name='Admin').prefetch_related('user_set', 'permissions')
    return render(request, "rbac/role_users_permissions.html", {"groups": groups})


@login_required
@csrf_exempt
def ajax_loaddata_email(request):
    user_filter = lambda user: {'company_id': user.company_id}
    return check_field_exists(request, User, 'email', user_filter=user_filter)

@login_required
@csrf_exempt
def userLoaddataUsername(request):
    user_filter = lambda user: {'company_id': user.company_id}
    return check_field_exists(request, User, 'username', user_filter=user_filter)
