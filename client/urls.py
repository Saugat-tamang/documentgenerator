from . import views
from django.urls import path

urlpatterns = [
    # START CLIENT ULRS
    path('client/add/', views.client_create, name='client.create'),
    path('list/', views.client_list, name='client.list'),
    path('client/json/', views.client_list_json, name='client_list_json'),
    path('store/', views.client_store, name='client.store'),
    path('edit/<int:id>/', views.client_edit, name='client.edit'),
    path('update/<int:id>/', views.client_update, name='client.update'),
    path('delete/<int:id>/', views.client_delete, name='client.delete'),
    # END CLIENT ULRS

    # START CLIENT EXCEL IMPORT AND EXPORT ULRS
    path('add/import/', views.client_create_import, name='client.import.create'),
    path('export/clientdemo/', views.export_clients_to_excel, name='export_client_demo'),
    path('import/clientexcel/', views.import_client_excel, name='import_client_excel'),
    path('client-details/<int:client_id>', views.client_details, name='client_details'),
    path('client/vat/status_chang/', views.client_vat_status_change, name='client.status.change'),

    # =======================
    # CLIENT EXCEL VALIDATION
    # =======================
    path('clients/import/', views.import_excel_client, name='clients.import'),
    path('clients/import/preview/', views.import_preview_client, name='clients.import.preview'),
    path('clients/import/save/', views.import_save_client, name='clients.import.save'),
 
]
