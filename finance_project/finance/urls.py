from django.urls import path
from .views import UserCreateView, CustomerView, TransactionView,MyTokenObtainPairView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('customers/', CustomerView.as_view(), name='customer-list-create'),
    path('transactions/', TransactionView.as_view(), name='transaction-list-create'),
    path('login/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
