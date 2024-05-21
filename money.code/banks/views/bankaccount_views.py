# Create your views here.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from django.views import generic

from calendar import monthrange
from datetime import date

from banks.models import BankAccount, Operation
from .miscelanous import get_view_day


########### BankAccount views ###################

@method_decorator(login_required, name='dispatch')
class BankAccountList(generic.ListView):
    """
    Display all active (close_date not reached) bank account and their respective
    checked, done and upcoming amount sum.
    """
    model = BankAccount
    template_name = 'banks/bankaccount_list.html'
    context_object_name = 'accounts'

    def get_context_data( self, **kwargs ):
        """
        send page title, selected item in the nav bar (menu) and view day context
        to the template.
        """
        context = super().get_context_data(**kwargs)
        context['types'] = BankAccount.objects.values('account_type')\
        .distinct()\
        .order_by('account_type')
        
        view_day = get_view_day( self.request )
        context['view_day'] = view_day
        context['menu'] = "banks"

        context['checked_sum'] = Operation.objects\
        .filter( Q(state="C") & Q(value_date__lte=view_day) )\
        .aggregate( total=Sum('amount') )['total']

        context['done_sum'] =  Operation.objects\
        .filter( Q(state__in=["C","D"]) & Q(value_date__lte=view_day) )\
        .aggregate( total=Sum('amount') )['total']

        context['upcoming_sum'] =  Operation.objects\
        .filter( Q(value_date__lte=view_day) )\
        .aggregate( total=Sum('amount') )['total']

        return context

    def get_queryset(self):
        """
        Elaborate the query set with bank account name and checked, done, upcoming amount sum.
        This is done for the hope paired values : view_year and view_month. If there are not set,
        today is use.
        """
        view_day = get_view_day( self.request )

        (first_day, nb_days) = monthrange( view_day.year, view_day.month )
        view_day = date( view_day.year, view_day.month, nb_days)

        checked = Sum( 'paymedia__operation__amount',
        filter=Q(paymedia__operation__value_date__lte=view_day) &
               Q( paymedia__operation__state="C" )  )

        done = Sum( 'paymedia__operation__amount',
        filter=Q(paymedia__operation__value_date__lte=view_day ) &
               Q( paymedia__operation__state__in=["C","D"]) )

        upcoming=Sum( 'paymedia__operation__amount',
        filter=Q(paymedia__operation__value_date__lte=view_day) )

        qs = BankAccount.objects\
        .filter( users=self.request.user )\
        .filter(close_date__gte=view_day)\
        .order_by( 'account_type' )\
        .annotate(checked=checked)\
        .annotate(done=done)\
        .annotate(upcoming=upcoming)
        return qs
