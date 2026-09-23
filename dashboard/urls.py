from . import views
from django.urls import path

urlpatterns = [
    # -----------------------------
    # Home & General Pages
    # -----------------------------
    path('', views.index, name='index'),
    path('dashboard_list/', views.index_list, name='index.list'),  
    # -----------------------------
    # Client Dashboard
    # -----------------------------
    path('client-dashboard/<int:client_id>/', views.client_dashboard, name='client_dashboard'),  
    path('exit-client-dashboard/', views.exit_client_dashboard, name='exit_client_dashboard'),  
    path('assignclienttouser/', views.assign_client_to_user, name='assign_client_to_user'), 
    path("update-dashboard/", views.update_dashboard, name="updatedashboard"), 

    # -----------------------------
    # Dashboard Configuration
    # -----------------------------
    path('dashboard/config/list/', views.dashboard_config_list, name='dashboardconfig.list'), 
    path('update/dashboard/config/', views.update_dashboard_config, name='update_dashboard_config'),
    path('dashboard/config/', views.dashboard_config_data, name='dashboard_config_data'),  

    # -----------------------------
    # API
    # -----------------------------
    path('api/clients/', views.api_clients, name='api_clients'),  # API endpoint for clients

]
