app_name = "user"
from . import views
from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.user_login_form, name='login'),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("verify-otp-page/", views.enter_otp_page, name="verify_otp_page"),
    path('authenticate/', views.auth_user, name='authenticate'),
    
    path('forgot-password/', views.forgot_password_request, name='forgot_password'),
    path('forgot-password/verify/', views.verify_forgot_otp, name='forgot_password.verify'),
    path('forgot-password/reset/', views.reset_password_form, name='forgot_password.reset'),
    path("forgot-password/resend-otp/", views.resend_forgot_otp, name="forgot_password.resend_otp"),

    
    path('auth/add/', views.add_user, name='user.create'),
    path('auth/user/store/', views.store_user, name='user.store.post'),
    path('list/', views.user_list, name='user.list'),
    path('auth/edit/<int:id>/', views.User_edit, name='user.edit'),
    path('auth/delete/<int:id>/', views.user_delete, name='user.delete'),
    path('auth/update/<int:id>/', views.user_update, name='user.update'),
    
    
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('userdetails', views.userDetails, name='user.details'),
    path('useredit/<int:id>', views.userEdit, name='user.details.edit'),
    path('upload/', views.upload_file, name='upload_file'),
    path('editprofile/<int:pk>', views.userprofile_edit, name='userprofile.edit'),
    path('updateprofile/<int:id>', views.userprofile_update, name='userprofile.update'),
    
    
    path("roleslist/", views.role_list_view, name="rolelist"),
    path("roles/create/", views.create_role_view, name="createrole"),
    path("roles/<int:role_id>/permissions/", views.assign_permissions_view, name="assignpermissions"),
    path("roles/<int:role_id>/users/", views.assign_users_view, name="assignusers"),
    path("role-users-permissions/", views.role_users_permissions_view, name="roleuserspermissions"),
    path('ajax/load-email', views.ajax_loaddata_email, name='ajax_user_validation_email'),
    path('ajax/usernamedata', views.userLoaddataUsername, name='ajax_loaddata_username'),   
]