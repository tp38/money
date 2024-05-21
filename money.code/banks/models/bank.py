from django.utils.translation import gettext_lazy as _
from django.db import models
from django import forms

class ColorWidget(forms.TextInput):
    input_type = 'color'
    template_name = 'banks/forms/widgets/color.html'


class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

        def formfield(self, **kwargs):
            kwargs['widget'] = ColorWidget
            return super(ColorField, self).formfield(**kwargs)

############### Bank ############################################
class Bank( models.Model):
    """
    This model is use to store bank data in the database
    """
    name = models.CharField( max_length=50 )
    short = models.CharField( max_length=5 )
    color = ColorField(default='#ffffff')
    logo = models.ImageField(upload_to='banks/logos', blank=True)

    def __str__(self):
        """
        string representation of a bank account
        """
        return f"{ '_'.join( self.name.split( ' ' ) )}"
