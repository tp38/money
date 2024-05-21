from django.utils.translation import gettext as _

from django.views import generic
from django.urls import reverse
from django.db.models import Sum


from banks.views import get_view_day

from budget.models import BudgetItemRef


class BudgetItemRefList(generic.ListView):
    """
    Display BudgetItemRef.
    """
    model = BudgetItemRef
    template_name = 'banks/budgetitemref_list.html'
    context_object_name = 'budgetitemref_list'

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu), mode (full or month list) and
        view day to the template.
        """
        context = super().get_context_data(**kwargs)
        context['view_day'] = get_view_day(self.request)

        qs = BudgetItemRef.objects.all().aggregate(total=Sum('amount'))
        context['solde'] = qs['total']
        context['menu'] = "budget"
        return context

    def get_queryset(self):
        """
        Elaborate the Hashtag list query set in the 2 modes (full or month list).
        """
        view_day = get_view_day( self.request )

        qs = BudgetItemRef.objects.all().order_by( 'name')
        return qs
