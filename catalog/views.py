from django.shortcuts import render
from django.views import generic
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User


# Create your views here.

from .models import Card, Account, ATM

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_cards = Card.objects.all().count()
    num_accounts = Account.objects.all().count()
    

 # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1



    context = {
        'num_cards': num_cards,
        'num_accounts': num_accounts,
  
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
    
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class CardListView(generic.ListView):
    model = Card
    context_object_name = 'my_card_list'   # your own name for the list as a template variable
    queryset = Card.objects # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Card
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    def get_queryset(self):
        return Card.objects.filter(account=self.request.user)
        
class CardDetailView(generic.DetailView):
    model = Card
    
class AccountDetailView(generic.DetailView):
    model = Account    

class ATMDetailView(generic.DetailView):
    model = ATM

    
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm, WithdrawTransactionForm, TransferTransactionForm, UserAccountCreationForm, AdminAccountCreationForm

@login_required
#@permission_required('catalog.can_mark_returned', raise_exception=True)
def transfer_card_user(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    card_instance = get_object_or_404(Card, pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            card_instance = form.cleaned_data['transfer_amount']
            card_instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-borrowed') )
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_transfer_amount = 5
        form = RenewBookForm(initial={'transfer_amount': proposed_transfer})
    context = {
        'form': form,
        'card_instance': card_instance,
    }
    return render(request, 'catalog/transfer_card_user.html', context)
    
@login_required
def WithdrawTransactionView(request):
    if request.method == "POST":
        form = WithdrawTransactionForm(request.user, request.POST)
        if form.is_valid():
            response_code = form.withdraw_amount()
            if form.redirect:
                if response_code == 1:
                #not enough money in account
                    print("MONEY ERROR")
                    return HttpResponseRedirect(reverse('my-cards') )
                elif response_code == -1:
                #not enough money in atm
                    print("ATM ERORR")
                    return HttpResponseRedirect(reverse('my-details') )
            else:
                print("Success")
                return HttpResponseRedirect(reverse('index') )

    form = WithdrawTransactionForm(request.user)
    context = {
         'form' : form,
    }
    return render(request, "catalog/withdraw.html", context=context)


@login_required
def TransferTransactionView(request):
    if request.method == "POST":
        form = TransferTransactionForm(request.user, request.POST)
        if form.is_valid():
            response_code = form.transfer_amount()
            if form.redirect:
                if response_code == 1:
                #not enough money in account
                    print("MONEY ERROR")
                    return HttpResponseRedirect(reverse('my-cards') )
                elif response_code == -1:
                #not enough money in atm
                    print("TARGET ERORR")
                    return HttpResponseRedirect(reverse('my-details') )
            else:
                print("Success")
                return HttpResponseRedirect(reverse('index') )

    form = TransferTransactionForm(request.user)
    context = {
         'form' : form,
    }
    return render(request, "catalog/transfer.html", context=context)
    

class BalanceInqView(LoginRequiredMixin,generic.ListView):
    model = Account
    template_name ='catalog/balance.html'
    paginate_by = 10

    def get_queryset(self):
        return Account.objects.filter(bank_user=self.request.user)
        
        

class ATMListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.atm.can_view_atm'
    model = ATM
    template_name ='catalog/atms.html'
    paginate_by = 10
    def get_queryset(self):
        return ATM.objects.all()


def UserCreateAccountView(request):
    if request.method == "POST":
        form = UserAccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("index")


    form = UserAccountCreationForm
    context = {
         'form' : form,
    }
    return render(request, "catalog/admin_create_account.html", context=context)
    
    
from django.contrib.auth.decorators import user_passes_test
@user_passes_test(lambda u: u.is_staff)
def AdminCreateAccountView(request):
    if request.method == "POST":
        form = AdminAccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("index")


    form = AdminAccountCreationForm
    context = {
         'form' : form,
    }
    return render(request, "catalog/admin_create_account.html", context=context)

