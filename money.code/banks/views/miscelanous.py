
from django.shortcuts import redirect
from django.urls import reverse
from django.forms import model_to_dict

from banks.models import BankAccount, PayMedia, Operation

from datetime import date, timedelta
from calendar import monthrange

DEBUG = False

def get_view_day( request ) :
    """
    Return the view_day if define in the request else return today
    """
    try:
        if request.GET['date'] :
            rdate = request.GET['date']
        else :
            rdate = request.POST['date']
        (year,month,day) = rdate.split( '-' )
        (first_day, nb_days) = monthrange( int(year), int(month) )
        return date( int(year), int(month), nb_days )
    except KeyError :
        today = date.today()
        (first_day, nb_days) = monthrange( today.year, today.month )
        return date( today.year, today.month, nb_days )


def change_date( request ):
    """
    set the reference date (view date) to specified year-month.
    store this ['view_year' 'view_month'] paired values in a cookie to use later.
    """
    if request.GET['view_day'] :
        (year,month,day) = request.GET['view_day'].split('-')
        (first_day, nb_days) = monthrange( int(year), int(month) )
        view_day = date( int(year), int(month), nb_days )
    else :
        today = date.today()
        (first_day, nb_days) = monthrange( today.year, today.month )
        view_day = date( today.year, today.month, nb_days )

    return redirect( f"{reverse('banks:bankaccount-list')}?date={view_day.year}-{view_day.month}-{view_day.day}" )

########## functions ############################
# @receiver(user_logged_in)
def periodic_ops(sender, **kwargs):
    """
    This function is launch by user_logged_in signal.
    It is looking for periodic upcoming operations (state='U' and frequency<>'None' ) in the m+2 month.
    if there's no, clone in this month :
        - the monthly ops (frequency='M') from m-2 month
        - the quaterly ops (frequency='Q') from m-4 month // not implemented yet
        - the Halfyearly ops (frequency='H') from m-7 month // not implemented yet
        - the Yearly ops (frequency='Y') from m-13 month // not implemented yet
    """
    today = date.today()
    twomonthfar = today + timedelta( 65 )
    #### check if there's already Upcoming 2 months later #########
    start = date( twomonthfar.year, twomonthfar.month, 1)
    (first_day, nb_days) = monthrange( twomonthfar.year, twomonthfar.month )
    end = date( twomonthfar.year, twomonthfar.month, nb_days )
    upcoming_periodic_ops = Operation.objects.filter( value_date__gte=start).filter( value_date__lte=end).filter(state='U').exclude( frequency='N')
    save = True if not upcoming_periodic_ops else False
    ######## monthly : search for ref ops 2 months before ###########
    if DEBUG or not upcoming_periodic_ops :
        sm = today - timedelta(60)
        (first_day, nb_days) = monthrange( sm.year, sm.month )
        sm = date( sm.year, sm.month, 1)
        em = date( sm.year, sm.month, nb_days )
        monthly_ops = Operation.objects.filter( value_date__gte=sm).filter( value_date__lte=em).filter( frequency='M')
        for ops in monthly_ops:
            ####### copy each ops 4 (2+2) months later ################
            kwargs = model_to_dict(ops, exclude=['id'])
            tmp_pm = PayMedia.objects.get( id=kwargs["paymedia"] )
            kwargs["paymedia"] = tmp_pm
            new_instance = Operation.objects.create(**kwargs)
            new_date = ops.completion_date + timedelta( 125 )
            (first_day, nb_days) = monthrange( new_date.year, new_date.month )
            day = nb_days if ops.completion_date.day > nb_days else ops.completion_date.day
            new_instance.completion_date = date( new_date.year, new_date.month, day )
            new_instance.value_date = date( new_date.year, new_date.month, day )
            new_instance.state = 'U'
            if save :
                new_instance.save()
            else :
                print( f"{ops.id} : {ops} -> {new_instance}" )


# @receiver(user_logged_in)
def update_value_date(sender, **kwargs):
    """
    This function is launch by user_logged_in signal.
    It search for operations that aren't checked yet and change their value date to `today`.
    It's like a car sweeps. It's need to see all past operations in the current month.
    """
    today = date.today()
    ops_to_update = Operation.objects.filter( value_date__lt=today).filter( state__in=['D','U'] )
    for ops in ops_to_update:
        ops.value_date = today
        ops.save()
        print( f"{ops.pk} => {ops}" )
