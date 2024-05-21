from django.utils.translation import gettext_lazy as _

from django.db import models
from banks.models import Operation

class OpElement(models.Model) :
    operation = models.ForeignKey( 'banks.Operation', on_delete=models.CASCADE, default=1)
    categorie = models.ForeignKey( 'BudgetItem', on_delete=models.PROTECT, default=1, related_name='Categorie')
    amount = models.DecimalField( max_digits=9, decimal_places=2 )
    valid = models.BooleanField(default=True)

    def __str__(self):
        """
        string representation of a OpElement
        """
        return f"{self.id} : {self.categorie} [{self.amount}]"

    def get_date(self):
        """
        return the value date of the OpElement
        """
        return Operation.objects.get(id=self.operation).value_date
