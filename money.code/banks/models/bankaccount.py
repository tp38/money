from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from datetime import date

################ Bank Account ###################################
BOOTSTRAP_COLOR_CHOICE = {
('primary', _('Blue')),
('secondary', _('Grey')),
('success', _('Green')),
('danger', _('Red')),
('warning', _('Orange')),
('info', _('Cyan')),
('light', _('LightGrey')),
('dark', _('DarkGrey')),
}

ACCOUNT_TYPE_CHOICE = {
        ('CC', _('Checking Account')),
        ('LA', _('`A` Booklet')),
        ('LEP', _('Popular Booklet')),
        ('ESP', _('Cash Account')),
        ('SE', _('Stock Exchange')),
}

class BankAccount(models.Model):
    """
    This model is use to store bank account data in the database
    """
    owners = models.ManyToManyField( get_user_model(), default=None )
    users  = models.ManyToManyField( get_user_model(), default=None , related_name='accesses',  )
    bank = models.ForeignKey('Bank', on_delete=models.CASCADE, default=1)
    account_type = models.CharField(max_length=5, choices=sorted(ACCOUNT_TYPE_CHOICE), default='CC')
    iban = models.CharField(max_length=27, default="")
    close_date = models.DateField(default=date(2199, 12, 31))
    bootstrap_color = models.CharField( max_length=10, choices=sorted(BOOTSTRAP_COLOR_CHOICE), default='primary')

    @classmethod
    def create(cls, bank, iban_nb, user_name):
        """
        use to add the user to owners list and to users list
        """
        ba = cls(bank=bank, iban=iban_nb)
        ba.bank_name = bank.name
        ba.save()
        ba.owners.add( user_name )
        ba.users.add( user_name )
        ba.save()
        return ba

    def __str__(self):
        """
        string representation of a bank account
        """
        return f"{self.Slug()} [{self.iban}]"

    def get_absolute_url(self):
        """
        the url for a specified bank account id
        """
        return reverse('banks:bankaccount-detail', args=[str(self.id)])

    def own_by(self):
        if self.owners.all().count() > 1 :
            own_by = _("Joint")
        else :
            own_by = self.owners.all()[0].username
        return own_by

    def Slug(self):
        """
        Create a slug for a bank account
        """
        own_by = self.own_by()
        bn = u'_'.join( (self.account_type + ' ' + self.bank.short).split(' ') )
        return f"{bn}_{own_by}"
