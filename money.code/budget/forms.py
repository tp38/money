from django.utils.translation import gettext_lazy as _
from django import forms
from budget import models


class BudgetItemForm(forms.ModelForm):
	class Meta:
		model = models.BudgetItem
		fields = [
			'name',
            'amount' ]
		labels = {
			'name': _('Name'),
            'amount': _('Amount'), }
		help_texts = {
			'name': _("Set here the Budget Item name."),
			'amount': _('Set here the amount for this budget item.'), }


class OpElementForm(forms.ModelForm) :
	class Meta:
		model = models.OpElement
		fields = [
			'categorie',
			'amount',
			'valid' ]
		labels = {
			'categorie': _('BudgetItem'),
			'amount': _('Amount'),
			'valid' : _('Valid') }
		help_texts = {
			'categorie': _("Set her the budget concerned BudgetItem."),
			'amount': _("Set here the amount for this budget item."),
			'valid' : _("OpElement to take into account or not.")
		}
