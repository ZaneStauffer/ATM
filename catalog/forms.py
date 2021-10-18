from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from catalog.models import Account, Card, ATM

class RenewBookForm(forms.Form):
    transfer_amount = forms.IntegerField(help_text="Enter an amount to transfer.")
    def clean_transfer_amount(self):
    	data = self.cleaned_data['transfer_amount']
    	if data < 0:
    		raise ValidationError(_('Invalid amount.'))
    	return data


class WithdrawTransactionForm(forms.Form):
    amount = forms.IntegerField(min_value=1)
    account = forms.ModelChoiceField(queryset=Account.objects.all())
    atm = forms.ModelChoiceField(queryset=ATM.objects.all())

    def __init__(self, user, *args, **kwargs):
        super(WithdrawTransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(bank_user=user)
        self.redirect = False

    def withdraw_amount(self):
        amount = self.cleaned_data['amount']
        account = self.cleaned_data['account']
        atm = self.cleaned_data['atm']

        if amount > account.balance:
            self.redirect = True
            return 1
        elif amount > (atm.current_balance - atm.min_balance):
            self.redirect = True
            return -1
        else:
            account.balance -= amount
            account.save()
            atm.current_balance -= amount
            atm.save()
        return amount
        
class TransferTransactionForm(forms.Form):
    amount = forms.IntegerField(min_value=1)
    from_account = forms.ModelChoiceField(queryset=Account.objects.all())
    to_account = forms.ModelChoiceField(queryset=Account.objects.all())
    def __init__(self, user, *args, **kwargs):
        super(TransferTransactionForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.filter(bank_user=user)
        self.fields['to_account'].queryset = Account.objects.all()
        self.redirect = False
            
    def transfer_amount(self):
        amount = self.cleaned_data['amount']
        from_account = self.cleaned_data['from_account']
        to_account = self.cleaned_data['to_account']
        if amount > from_account.balance:
            self.redirect = True
            return 1
        else:
            from_account.balance -= amount
            from_account.save()
            to_account.balance += amount
            to_account.save()
        return amount

class UserAccountCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        
class AdminAccountCreationForm(ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'account_number', 'pin', 'address', 'balance', 'phone_number', 'bank_user')

