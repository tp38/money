# Create your views here.
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import generic
from django.db.models import Q, Count, Sum

from calendar import monthrange
from datetime import date, timedelta

from banks.models import BankAccount, Operation
from banks.forms import OperationForm, OperationSearchForm
from .miscelanous import get_view_day


def change_status(request, pk, status):
    """
    Set the operation state to checked (C)
    """
    op = Operation.objects.get( id= pk )
    op.value_date = date.today()
    op.state = status
    op.save()

    view_day = get_view_day( request )

    return redirect( f"{reverse('banks:operation-list', args = (op.paymedia.bank_account.id, 'active') ) }?date={view_day.year}-{view_day.month}-{view_day.day}" )


def search_operations(request, account_id ):
    """
    Define a search form (GET method) for operations. and do the search (POST method)
    with the user define strings. Sort operations by value_date decreasing.
    """
    if request.method == 'POST':
        form = OperationSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data :
                Qr = None
                for f_name,f_value in form.cleaned_data.items() :
                    if f_value :
                        if f_name == 'paymedia_id' :
                            q = Q(**{ f"{f_name}" : f_value } )
                        else :
                            q = Q(**{ f"{f_name}__contains" : f_value } )
                        if Qr:
                            Qr = Qr | q
                        else:
                            Qr = q
            ops = Operation.objects.all().filter( Qr ).order_by( '-value_date' )
            return render(request, 'banks/operation_list.html', {'operation_list': ops, 'menu': 'banks', 'bankaccount_id': account_id } )
    else:
        form = OperationSearchForm()
        return render(request, 'banks/operation_search_form.html', {'form': form, 'bankaccount_id': account_id, 'menu': 'banks' })


#-------------- generic views ---------------------------------------

class OperationList(generic.ListView):
    """
    Display operations for a specified bank account and a paired view_year, view_month.
    User could selected :
    - all operations with "checked" state
    - all operations with "done" state
    - all operations with "upcoming" state
    - all active (done + upcoming) operations
    """
    model = Operation
    template_name = 'banks/operation_list.html'
    context_object_name = 'operation_list'

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu), the bank account, the paired view_year
        view_month and the mode (checked, done,upcoming and active) to the template.
        """

        view_day = get_view_day( self.request )

        context = super().get_context_data(**kwargs)
        context['menu'] = "banks"
        context['bankaccount'] = BankAccount.objects.get( id=self.kwargs['pk']).Slug()
        context['bankaccount_id'] = self.kwargs['pk']
        context['view_day'] = get_view_day(self.request)
        context['mode'] = self.kwargs['mode']
        return context

    def get_queryset(self):
        """
        Elaborate the query set according the user choices
        (view_day and checked, done, upcoming or active mode).
        Sort operations by value_date decreasing.
        """
        view_day = get_view_day( self.request )

        start_day = date(view_day.year, view_day.month, 1)
        (first_day, nb_days) = monthrange( start_day.year, start_day.month )
        end_day = start_day + timedelta( nb_days - 1)

        if self.kwargs['mode']  == 'checked' :
            query_set = Operation.objects.filter(paymedia__bank_account__id = self.kwargs['pk'] ).filter( state = "C" ).filter(value_date__gte=start_day).filter(value_date__lte=end_day).annotate( nb=Count("opelement") ).annotate(total=Sum("opelement__amount")).order_by( '-value_date' )
        elif self.kwargs['mode']  == 'done' :
            query_set = Operation.objects.filter(paymedia__bank_account__id = self.kwargs['pk'] ).filter( state = "D" ).filter(value_date__lte=end_day).annotate( nb=Count("opelement") ).annotate(total=Sum("opelement__amount")).order_by( '-value_date' )
        elif self.kwargs['mode']  == 'upcoming' :
            query_set = Operation.objects.filter(paymedia__bank_account__id = self.kwargs['pk'] ).filter( state = "U" ).filter(value_date__lte=end_day).annotate( nb=Count("opelement") ).annotate(total=Sum("opelement__amount")).order_by( '-value_date' )
        elif self.kwargs['mode']  == 'active' :
            query_set = Operation.objects.filter(paymedia__bank_account__id = self.kwargs['pk'] ).filter( state__in=["U","D"] ).filter(value_date__lte=end_day).annotate( nb=Count("opelement") ).annotate(total=Sum("opelement__amount")).order_by( '-value_date' )
        else : # all records
            query_set = Operation.objects.filter(paymedia__bank_account__id = self.kwargs['pk'] ).filter(value_date__gte=start_day).filter(value_date__lte=end_day).annotate( nb=Count("opelement") ).annotate(total=Sum("opelement__amount")).order_by( '-value_date' )
        return query_set


class OperationCreate(generic.CreateView):
    """
    Create operation form
    """
    model = Operation
    form_class = OperationForm
    template_name = 'banks/operation_form.html'

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu), the view day and the bank account id
        to the template.
        """
        context = super().get_context_data(**kwargs)
        context['menu'] = "banks"
        context['view_day'] = get_view_day( self.request )
        context['bankaccount_id'] = self.kwargs['account_id']
        return context

    def get_form_kwargs(self):
        """
        Send the bank account id to the form to have a short list of paymedia.
        Only bank account paymedia are shown.
        """
        kwargs = super(OperationCreate, self).get_form_kwargs()
        kwargs.update({'bankaccount_id': self.kwargs.get('account_id')})
        return kwargs

    def get_success_url(self):
        """
        Define current (view_day) bank account all operation list as a success return url
        """
        view_day = get_view_day( self.request )
        return f"{reverse('banks:operation-list', args =(self.kwargs['account_id'], 'active') )}?date={view_day.year}-{view_day.month}-{view_day.day}"


class OperationDelete(generic.DeleteView):
    """
    Delete operation view (a confirm form is shown)
    """
    model = Operation

    def get_success_url(self):
        """
        Define current (view_day) bank account all operation list as a success return url
        """
        view_day = get_view_day( self.request )
        op = Operation.objects.get( id=self.kwargs['pk'] )

        return f"{reverse('banks:operation-list', args = (op.paymedia.bank_account.id, 'active') )}?date={view_day.year}-{view_day.month}-{view_day.day}"

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu) to the template.
        """
        context = super().get_context_data(**kwargs)
        context['menu'] = "banks"
        context['view_day'] = get_view_day( self.request )
        return context


class OperationUpdate(generic.UpdateView):
    """
    Create update operation form
    """
    model = Operation
    form_class = OperationForm
    template_name = 'banks/operation_form.html'

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu), the view day and the bank account id
        to the template.
        """
        context = super().get_context_data(**kwargs)
        op = Operation.objects.get(id=self.kwargs['pk'])
        context['menu'] = "banks"
        context['view_day'] = get_view_day( self.request )
        context['bankaccount_id'] = op.paymedia.bank_account.id
        return context

    def get_success_url(self):
        """
        Define current (view_day) bank account all operation list as a success return url
        """
        view_day = get_view_day( self.request )
        op = Operation.objects.get( id=self.kwargs['pk'] )

        return f"{reverse('banks:operation-list', args = (op.paymedia.bank_account.id, 'active') )}?date={view_day.year}-{view_day.month}-{view_day.day}"

    def get_form_kwargs(self):
        """
        Send the bank account id to the form to have a short list of paymedia.
        Only bank account paymedia are shown.
        """
        op = Operation.objects.get(id=self.kwargs['pk'])
        kwargs = super(OperationUpdate, self).get_form_kwargs()
        kwargs.update({'bankaccount_id': op.paymedia.bank_account.id })
        return kwargs
