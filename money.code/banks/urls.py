from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'banks'

urlpatterns = [
    path('change-date', views.change_date, name='change-date' ),
    path('accounts', views.BankAccountList.as_view(), name='bankaccount-list'),
    path('account/<int:pk>/ops/<str:mode>', views.OperationList.as_view(), name='operation-list'),
    path('account/<int:account_id>/operations/search', views.search_operations, name='operations-search'),
    path('account/<int:account_id>/operations/add', views.OperationCreate.as_view(), name='operation-add'),
    path('operation/<int:pk>/delete', views.OperationDelete.as_view(), name='operation-del'),
    path('operation/<int:pk>/edit', views.OperationUpdate.as_view(), name='operation-edit'),
    path('operation/<int:pk>/changestatus/<str:status>', views.change_status, name='operation-change-status'),

]

admin.site.site_url = "/banks/accounts"
