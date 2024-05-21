import re

from django.core.exceptions import ObjectDoesNotExist

from budget.models import Month, BudgetItem, BudgetItemRef, OpElement
from banks.models import Operation
from datetime import date

def get_month( view_day ) :
    try :
        m = Month.objects.get( start=date(view_day.year,view_day.month,1) )
    except ObjectDoesNotExist :
        create_items( date(view_day.year,view_day.month,1) )
        m = Month.objects.get( start=date(view_day.year,view_day.month,1) )
    return m


def create_items( month ) :
    thismonth = month.replace( day=1 )

    m = Month.objects.filter( start=thismonth )
    if m.count() == 0 :
        bud = Month(start=thismonth)
        bud.save()
    else :
        bud = m[0]

    items = BudgetItem.objects.filter( month=bud )
    if items.count() == 0 :
        refs = BudgetItemRef.objects.all()
        for ar in refs :
            bi = BudgetItem( name=ar.name, amount=ar.amount, month=bud )
            bi.save()
