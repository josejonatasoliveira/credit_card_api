from django.urls import path
from . import views

urlpatterns = [
    path('cards/', views.CreditCardListView.as_view(), name='credit-card-list'),
    path('encrypt-credit-card/', views.encrypt_credit_card, name='encrypt-credit-card'),
    path('cards/<int:card_id>/', views.get_credit_card_details, name='credit-card-detail'),
]