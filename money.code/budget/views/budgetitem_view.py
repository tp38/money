from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist

from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Sum, F


from banks.views import get_view_day

from budget.models import Month, BudgetItem, OpElement
from budget.forms import BudgetItemForm
from .miscelanous import get_month



class BudgetItemList(generic.ListView):
    """
    Display BudgetItem.
    """
    model = BudgetItem
    template_name = 'budget/budgetitem_list.html'
    context_object_name = 'budgetitem_list'

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu), mode (full or month list) and
        view day to the template.
        """
        context = super().get_context_data(**kwargs)
        view_day = get_view_day(self.request)
        context['view_day'] = view_day

        m = get_month( view_day )

        q = BudgetItem.objects.filter(month=m)
        context['solde'] = q.aggregate(total=Sum('amount'))['total']
        context['actual'] = OpElement.objects\
        .filter(categorie__in=q)\
        .filter(valid=True)\
        .aggregate(total=Sum('amount'))['total']

        context['menu'] = "budget"
        return context

    def get_queryset(self):
        """
        Elaborate the BudgetItem list query set.
        """
        view_day = get_view_day( self.request )
        m = get_month( view_day )

        qs = OpElement.objects\
        .values('categorie__id','categorie__month__start',
        'categorie__name', 'categorie__amount', 'valid')\
        .filter(valid=True)\
        .filter(categorie__month__start=view_day.replace(day=1))\
        .annotate(montant=Sum('amount'))\
        .annotate(delta=F('categorie__amount')-F('montant'))\
        .order_by('categorie__name')

        return qs




class BudgetItemUpdate(generic.UpdateView):
    """
    Create budget item form
    """
    model = BudgetItem
    form_class = BudgetItemForm
    template_name = 'budget/budgetitem_form.html'

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu) to the template.
        """
        context = super().get_context_data(**kwargs)
        view_day = get_view_day( self.request )
        context['view_day'] = view_day
        context['menu'] = "budget"
        context['bi_id'] = self.get_object().id
        return context

    def get_success_url(self):
        """
        Define current (view_day) bank account all operation list as a success return url
        """
        view_day = get_view_day( self.request )
        return f"{reverse('budget:items-list')}?date={view_day.year}-{view_day.month}-{view_day.day}"
