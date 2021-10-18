from django.contrib import admin

# Register your models here.


from .models import Card, Account, ATM

admin.site.register(Card)
admin.site.register(Account)
admin.site.register(ATM)


#@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('card', 'date_issued', 'account', 'balance', 'id')
    list_filter = ('balance')
    
    
