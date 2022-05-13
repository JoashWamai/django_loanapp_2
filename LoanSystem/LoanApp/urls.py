from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),

    path("loanapplication/", views.loanapplication, name='application'),
    path("customerinformation/<int:pk>/", views.customerinformation, name='cust_info'),
    path("loans/", views.loans, name='all_loans'),
    path("customers/", views.customerlist, name='all_customers'),
    path("updatecustomer/<int:pk>", views.updatecustomer, name='update_customer'),
    path("customerreport/<int:pk>", views.customerinfopdf, name='cust_report'),
    path("loanaction/", views.loanapproval, name='loan_action'),
    path("search/", views.search, name="search"),

    path("payment/", views.payment, name='payment'),
    path("paymentform/", views.paymentform, name='payment_form'),
    path("payments/", views.paymentlist, name='all_payment'),

    path("settings/", views.settings, name="settings"),
    path("loanstatusgraph/", views.statusgraph, name="statusgraph"),
    path("businesstypegraph/", views.businesstypegraph, name="typegraph"),

    path("disbursement/<int:pk>/", views.disburse, name='disburse'),

]
