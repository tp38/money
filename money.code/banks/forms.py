from django.utils.translation import gettext_lazy as _
from django import forms
from banks import models
from banks.models import PayMedia

from datetime import date

class OperationForm(forms.ModelForm):
	completion_date = forms.DateField(
			initial=date.today(),
			label=_('Completion date'),
			help_text=_('Enter here the completion date for this operation.'),
			widget=forms.TextInput(
					attrs={'type': 'date'}
				)
	)
	amount = forms.DecimalField(
			localize=True,
			label=_('Amount'),
			help_text=_('-999999.99€ <= the amount in euro (€) <= 999999.99€.'),
	)

	def __init__(self, *args, **kwargs):
		ba = kwargs.pop('bankaccount_id')
		super(OperationForm, self).__init__(*args, **kwargs)
		self.fields['paymedia'].queryset = PayMedia.objects.filter(bank_account=ba)

	class Meta:
		model = models.Operation
		fields = [
			'paymedia',
			'completion_date',
			'comment',
			'amount',
			'state',
			'frequency' ]
		labels = {
			'paymedia': _('Paymedia'),
			'comment': _('Comment'),
			'state': _('State'),
			'frequency': _('Reccurence') }
		help_texts = {
			'paymedia': _('PayMedia for this Operation.'),
			'comment': _('Write here anything that make sense for you.\nUse @Pseudo ou #HashTag to sort Operations.'),
			'state': _("State of operation in ['Check', 'Done', 'Upcoming']."),
			'frequency': _("Frequency of operation in ['None', 'Monthly', 'Quaterly', 'Halfyearly', 'Yearly']") }



class OperationSearchForm(forms.Form):
	state_choices = [('', '---' )] + models.STATE_CHOICE
	frequency_choices = [('', '---' )] + models.FREQUENCY_CHOICE
	paymedia_id = forms.ModelChoiceField(queryset=models.PayMedia.objects.all(),required=False, label=_('PayMedia'), help_text=_('Choose here the paymedia you search for'))
	completion_date = forms.DateField(required=False, label=_('Completion_date'), help_text=_('Enter here the completion date you search for'), widget=forms.TextInput( attrs={'type': 'date'} ) )
	value_date = forms.DateField(required=False, label=_('Value date'), help_text=_('Enter here the value date you search for'), widget=forms.TextInput( attrs={'type': 'date'} ) )
	comment = forms.CharField(required=False, label=_('Comment'), help_text=_('Enter here the string you search for in Comment field') )
	amount = forms.DecimalField(max_digits=9, decimal_places=2, required=False, label=_('Amount'), help_text=_('Enter here the amount you search for') )
	state = forms.ChoiceField( choices=state_choices , required=False, label=_('State'), help_text=_('Select the state you search for') )
	frequency = forms.ChoiceField( choices=frequency_choices , required=False, label=_('Recurrence'), help_text=_('Select the recurrence you search for') )
