from django.urls import path

from . import views

app_name = 'budget'
urlpatterns = [
    path('itemrefs/', views.BudgetItemRefList.as_view(), name='itemrefs-list'),
    path('items/', views.BudgetItemList.as_view(), name='items-list'),
    path('item/<int:pk>/update', views.BudgetItemUpdate.as_view(), name='item-update'),
    path('item/<int:pk>/elts', views.OpElementsForBudgetItemList.as_view(), name='elts4bi-list' ),
    path('operation/<int:pk>/elts', views.OpElementsForOperationList.as_view(), name='elts4op-list' ),
    path('operation/<int:pk>/eltadd', views.OpElementCreate.as_view(), name='element-add' ),
    path('elt/<int:pk>/update', views.OpElementUpdate.as_view(), name='element-update'),
    path('elt/<int:pk>/delete', views.OpElementDelete.as_view(), name='element-delete'),
    path('enveloppes/', views.EnveloppePageView.as_view(), name='enveloppes'),
    path('enveloppes/<str:categorie>', views.EnveloppeDetailView.as_view(), name='enveloppe-detail'),
]
