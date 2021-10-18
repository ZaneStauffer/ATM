from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User


# Create your models here.


class Account(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    name = models.CharField(max_length=100, null=False,default="Test")
    account_number = models.IntegerField(unique=True, primary_key=True)
    #email = models.CharField(max_length=100, null=False,default="test@gmail.com")
    #password = models.CharField(max_length=100, null=False,default="Test123!")
    pin = models.IntegerField()
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    balance = models.IntegerField(null=False, default = 0)
    bank_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    


    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('account-detail', args=[str(self.id)])
        
        

class Card(models.Model):
    owner = models.CharField(max_length=100, null=False,default="Test")
    date_issued = models.DateField(null=True)
    date_expires = models.DateField(null=True)
    #balance = models.IntegerField()
    account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    

    
    def __str__(self):
        """String for representing the Model object."""
        return self.owner

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('card-detail', args=[str(self.id)])
        
        
import uuid

class ATM(models.Model):
    atm_number = models.IntegerField(unique= True, null=False, primary_key=True)
    address = models.CharField(max_length=100, null=False,default="Test Location")
    status = models.CharField(max_length=100, null=False,default="Available")
    last_refill = models.DateField(null=True)
    next_refill = models.DateField(null=True)
    min_balance = models.IntegerField(default = 0)
    current_balance = models.IntegerField(default=100)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.address

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('atm-detail', args=[str(self.atm_number)])
	
	
        
        
  
