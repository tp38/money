from django.utils.translation import gettext_lazy as _

from django.db import models
from datetime import date

from .month import Month


class BudgetItem(models.Model) :
    """
    A BudgetItem associate an amount with one or more HashTag within a Budget
    """
    name = models.CharField(max_length=30)
    amount = models.DecimalField( max_digits=9, decimal_places=2 )
    month = models.ForeignKey('Month', on_delete=models.CASCADE, default=1, related_name='Month')

    def __str__(self):
        """
        string representation of a bank account
        """
        return f"{self.month}.{self.name} [{self.amount}]"
