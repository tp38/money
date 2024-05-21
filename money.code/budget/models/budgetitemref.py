from django.utils.translation import gettext_lazy as _

from django.db import models


class BudgetItemRef(models.Model) :
    """
    A BudgetItemRef as
    """
    name = models.CharField(max_length=30)
    amount = models.DecimalField( max_digits=9, decimal_places=2 )

    def __str__(self):
        """
        string representation of a bank account
        """
        return f"{self.name} [{self.amount}]"
