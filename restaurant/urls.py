from django.urls import path
from .views import Dashboard, OrderDetails, Logout

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('orders/<int:pk>/', OrderDetails.as_view(), name='order-details'),
    path('dashboard/logout', Logout.as_view(), name='logout'),
]
