
from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('cards/', views.CardListView.as_view(), name='cards'),
]

urlpatterns += [
    path('', views.index, name='index'),
    path('cards/', views.CardListView.as_view(), name='cards'),
    path('card/<int:pk>', views.CardDetailView.as_view(), name='card-detail'),
]


urlpatterns += [

    path('atm/<int:pk>', views.ATMDetailView.as_view(), name='atm-detail'),
]




urlpatterns += [
    path('card/<int:pk>/transfer/', views.transfer_card_user, name='transfer-card-user'),
]

urlpatterns += [
    path('withdraw/', views.WithdrawTransactionView, name='withdraw'),
]

urlpatterns += [
    path('transfer/', views.TransferTransactionView, name='transfer'),
]

urlpatterns += [
    path('balance/', views.BalanceInqView.as_view(), name='balance'),
]

urlpatterns += [
    path('', views.index, name='index'),
    path('accounts/', views.CardListView.as_view(), name='accounts'),
    path('accounts/<int:pk>', views.AccountDetailView.as_view(), name='account-detail'),
]


urlpatterns += [
    path('mycards/', views.LoanedBooksByUserListView.as_view(), name='my-cards'),
]

urlpatterns += [
    path('atms/', views.ATMListView.as_view(), name='atms'),

]

urlpatterns += [
    path('create_account/', views.UserCreateAccountView, name='create-account'),

]


urlpatterns += [
    path('admin_create_account/', views.AdminCreateAccountView, name='admin-create-account'),

]

