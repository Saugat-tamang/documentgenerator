from . import views
from django.urls import path

urlpatterns = [
    # Fiscal Year URLS
    path('fiscal/list/', views.fiscal_list, name='fiscal.list'),
    path('fiscal/add/', views.fiscal_create, name='fiscal.create'),
    path('fiscal/store/', views.fiscal_store, name='fiscal.store'),
    path('fiscal/edit/<int:id>/', views.fiscal_edit, name='fiscal.edit'),
    path('fiscal/update/<int:id>/', views.fiscal_update, name='fiscal.update'),
    path('fiscal/delete/<int:id>/', views.fiscal_delete, name='fiscal.delete'),
    path('changefiscal/', views.change_fiscalyear, name='fiscal.changefiscalyear'),
    path('updatefiscal/', views.update_fiscalyear, name='fiscal.updatefiscalyear'),
    path('realtime/fisicalyear/',views.realtime_validation_fisicalyear,name='realtime_validation_fisicalyear'),
    
    #client fiscal year update
    path('updateclientfiscal/', views.update_client_fiscalyear, name='update_client_fiscalyear'),
    path('company/changeclientfiscal/', views.change_client_fiscalyear, name='change_client_fiscalyear'),

    # Company URLS
    path('list/', views.company_list, name='company.list'),
    path('add/', views.company_create, name='company.create'),
    path('store/', views.company_store, name='company.store'),  
    path('edit/<int:id>/', views.company_edit, name='company.edit'),
    path('update/<int:id>/', views.company_update, name='company.update'),
    path('delete/<int:id>/', views.company_delete, name='company.delete'),
    path('ajax/load-companyname', views.ajax_loaddata_companyname, name='ajax_loaddata_companyname'),
    path('ajax/load-companypan', views.ajax_loaddata_companypan, name='ajax_loaddata_companypan'),

]
