from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Sum


from banks.views import get_view_day

from budget.models import OpElement



class EnveloppePageView(TemplateView):
    template_name = "budget/enveloppes_list.html"

    def get_context_data(self, **kwargs):
        view_day = get_view_day(self.request)

        context = super().get_context_data(**kwargs)
        context['view_day'] = view_day
        context['menu'] = "budget"
        context["enveloppes"] = OpElement.objects.filter( valid=False)\
        .filter( categorie__month__start__gte = '2023-09-01' )\
        .filter( categorie__month__start__lte = view_day.replace(day=1) )\
        .values( 'categorie__name' )\
        .annotate( total=Sum('amount') )\
        .order_by( 'categorie__name' )
        return context



class EnveloppeDetailView(TemplateView):
    template_name = "budget/enveloppe_detail.html"


    def get_context_data(self, **kwargs):
        view_day = get_view_day(self.request)

        context = super().get_context_data(**kwargs)
        context['view_day'] = view_day
        context['menu'] = "budget"
        context["enveloppe"] = OpElement.objects.filter( valid=False)\
        .filter( categorie__month__start__gte = '2023-09-01' )\
        .filter( categorie__month__start__lte = view_day.replace(day=1) )\
        .filter( categorie__name = kwargs['categorie'] )\
        .order_by( '-categorie')
        return context
