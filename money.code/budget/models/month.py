from django.utils.translation import gettext_lazy as _

from django.db import models
from datetime import date


class Month(models.Model) :
    """
    A Month is a tag for collecting BudgetItems for a particular month.
    """

    start = models.DateField(default=date(2199, 12, 1))

    def __str__(self):
        """
        string representation of Budget
        """
        return f"{self.start.year}-{self.start.month:02}"
