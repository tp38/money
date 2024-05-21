from django.views import generic
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


from banks.models import Operation
from banks.views import get_view_day
from budget.models import OpElement, Month, BudgetItem
from budget.forms import OpElementForm
from budget.views import create_items



class OpElementsForBudgetItemList(generic.ListView):
    """
    Display OpElement list for a specified operation.
    """
    model = OpElement
    template_name = 'budget/elts4bi_list.html'
    context_object_name = 'opelement_list'

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu), mode (full or month list) and
        view day to the template.
        """
        context = super().get_context_data(**kwargs)
        view_day = get_view_day(self.request)
        context['view_day'] = view_day
        context['menu'] = "budget"
        context['bi'] = BudgetItem.objects.get(id=self.kwargs['pk'] )
        return context

    def get_queryset(self):
        """
        Elaborate the OpElement list query set.
        """
        bi = BudgetItem.objects.get(id=self.kwargs['pk'] )
        qs = OpElement.objects.filter( categorie=bi ).filter(valid=True)
        return qs



class OpElementsForOperationList(generic.ListView):
    """
    Display OpElement list for a specified operation.
    """
    model = OpElement
    template_name = 'budget/elts4op_list.html'
    context_object_name = 'opelement_list'

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu), mode (full or month list) and
        view day to the template.
        """
        context = super().get_context_data(**kwargs)
        view_day = get_view_day(self.request)
        context['view_day'] = view_day
        context['menu'] = "budget"
        context['operation'] = Operation.objects.get(id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        """
        Elaborate the OpElement list query set.
        """
        oi = self.kwargs['pk']
        qs = OpElement.objects.filter(operation__id=oi).order_by('categorie')
        return qs



class OpElementDelete(generic.DeleteView):
    """
    Delete OpElement view (a confirm form is shown)
    """
    model = OpElement

    def get_success_url(self):
        """
        Define current (view_day) bank account all operation list as a success return url
        """
        view_day = get_view_day( self.request )
        return f"{reverse('budget:items-list')}?date={view_day.year}-{view_day.month}-{view_day.day}"

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu) to the template.
        """
        view_day = get_view_day( self.request )

        context = super().get_context_data(**kwargs)
        context['menu'] = "budget"
        return context


class OpElementUpdate(generic.UpdateView):
    """
    Create update OpElement form
    """
    model = OpElement
    form_class = OpElementForm
    template_name = 'budget/opelement_form.html'

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu), the view day and the bank account id
        to the template.
        """
        context = super().get_context_data(**kwargs)

        view_day = get_view_day( self.request )
        context['view_day'] = view_day

        bud = Month.objects.get( start=view_day.replace(day=1) )
        context['form'].fields['categorie'].queryset = BudgetItem.objects.filter( month=bud ).order_by('name')
        context['menu'] = "budget"
        return context

    def form_valid( self, form) :
        form.instance.operation = OpElement.objects.get( id = self.kwargs['pk'] ).operation
        return super().form_valid(form)


    def get_success_url(self):
        """
        Define current (view_day) bank account all operation list as a success return url
        """
        view_day = get_view_day( self.request )
        return f"{reverse('budget:items-list')}?date={view_day.year}-{view_day.month}-{view_day.day}"


class OpElementCreate(generic.CreateView):
    """
    Create operation form
    """
    model = OpElement
    form_class = OpElementForm
    template_name = 'budget/opelement_form.html'

    def get_context_data( self, **kwargs ):
        """
        send selected item in the nav bar (menu), the view day and the bank account id
        to the template.
        """
        context = super().get_context_data(**kwargs)
        view_day = get_view_day( self.request )
        context['view_day'] = view_day

        try :
            bud = Month.objects.get( start=view_day.replace(day=1) )
        except ObjectDoesNotExist :
            create_items( view_day )
            bud = Month.objects.get( start=view_day.replace(day=1) )

        context['form'].fields['categorie'].queryset = BudgetItem.objects.filter( month=bud ).order_by('name')
        context['menu'] = "budget"
        return context

    def form_valid( self, form) :
        form.instance.operation = Operation.objects.get( id = self.kwargs['pk'] )
        return super().form_valid(form)


    def get_success_url(self):
        """
        Define current (view_day) bank account all operation list as a success return url
        """
        view_day = get_view_day( self.request )
        return f"{reverse('budget:items-list')}?date={view_day.year}-{view_day.month}-{view_day.day}"
