from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse

from datetime import date, timedelta

###################### Operation ########################

STATE_CHOICE = [
        ('C', _('Check')),
        ('D', _('Done')),
        ('U', _('Upcoming')),
]

FREQUENCY_CHOICE = [
        ('N', _('None')),
        ('M', _('Monthly')),
        ('Q', _('Quaterly')),
        ('H', _('Halfyearly')),
        ('Y', _('Yearly')),
]

class Operation(models.Model):
    """
    This model is use to store Operation data in the database
    """
    paymedia = models.ForeignKey('PayMedia', on_delete=models.CASCADE, default=1)
    completion_date = models.DateField()
    value_date = models.DateField()
    old_id = models.IntegerField(default=-1)
    comment = models.CharField(max_length=100)
    amount = models.DecimalField( max_digits=9, decimal_places=2 )
    state = models.CharField( max_length=1, choices=STATE_CHOICE, default='U')
    frequency = models.CharField( max_length=1, choices=FREQUENCY_CHOICE, default='N')

    def save(self, *args, **kwargs):
        """
        use to calculate the value_date from completion_date
        """
        pm = self.paymedia
        if pm.debit_type == 'D' :
            self.value_date = pm.get_deferred_date( self.completion_date )
        else:
            self.value_date = self.completion_date

        today = date.today()
        if ( self.state != 'C' ) and ( self.value_date < today ) :
            self.value_date = today
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation for an Operation
        """
        return f"{self.value_date} [{self.paymedia.media_type} D{self.paymedia.debit_type}] : {self.comment} = {self.amount}"

    def get_absolute_url(self):
        """
        the url for a specified operation id
        """
        return reverse('banks:operation-detail', args=[str(self.bank_account.id),str(self.id)])
