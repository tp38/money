from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse

from math import ceil
from calendar import monthrange
from datetime import date, timedelta

###################### PayMedia #########################

DEBIT_TYPE_CHOICE = [
        ('I', _('Immediate')),
        ('D', _('Deferred')),
]

MEDIA_TYPE_CHOICE = [
        ('CB', _('Card')),
        ('CHQ', _('Cheque')),
        ('VRT', _('Transfer')),
        ('ESP', _('Cash')),
        ('TIP', _('Interbank'))
]

class PayMedia(models.Model):
    """
    This model is use to store PayMedia data in the database
    """
    bank_account = models.ForeignKey('BankAccount', on_delete=models.CASCADE, default=1)
    media_type = models.CharField(max_length=3, choices=MEDIA_TYPE_CHOICE, default="CB")
    comment = models.CharField(max_length=200)
    debit_type = models.CharField( max_length=1, choices=DEBIT_TYPE_CHOICE, default='I')
    care_day = models.PositiveSmallIntegerField(default=20)
    nb_deferred_days = models.PositiveSmallIntegerField(default=40)
    expire_date = models.DateField(default=date(2199, 12, 31))

    def __str__(self):
        """
        String representation for a paymedia
        """
        return f"{self.bank_account.Slug()} - {self.media_type} D{self.debit_type}"

    def get_absolute_url(self):
        """
        the url for a specified paymedia id
        """
        return reverse('banks:paymedia-detail', args=[str(self.bank_account.id),str(self.id)])

    def Slug(self):
        """
        Create a slug for a paymedia
        """
        return f"{self.media_type}_D{self.debit_type}_{self.bank_account.Slug()}"

    def get_deferred_date(self, a_date):
        """
        calcultate the value date for an operation with deferred paymedia
        """
        add_month = ceil(self.nb_deferred_days/30)
        v_date = date( a_date.year, a_date.month, 1)
        i = 0
        if a_date.day > self.care_day :
            add_month += 1
        while i < add_month :
            (first_day, nb_days) = monthrange( v_date.year, v_date.month )
            v_date += timedelta ( nb_days )
            i += 1
        return v_date
