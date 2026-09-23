from . import views
from django.urls import path

urlpatterns = [
  path('create/', views.auditlogCreate, name='auditlog.create'),
  path('list/', views.auditlogList, name='auditlog.list'),
]
