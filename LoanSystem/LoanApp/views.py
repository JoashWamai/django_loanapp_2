from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
import sweetify
from .forms import *
import random
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.db.models import Count


@login_required(login_url='register')
def home(request):
    customer_total = Customer.objects.all().count()
    loan_total = Loan.objects.filter(status="Disbursed").count()
    loans_all = Loan.objects.all().order_by("-DateCreated")[:5]
    payment_all = Payment.objects.all().order_by('-DatePaid')[:5]
    payment_count = Loan.objects.filter(status="Paid").count()
    context = {"customer_count": customer_total, 'loan_count': loan_total, 'loans': loans_all, 'payments': payment_all,
               "payment_count": payment_count}

    return render(request, 'loanapp/home.html', context)


@login_required(login_url='register')
@allowed_users(['officer'])
def loanapplication(request):
    custform = CustomerForm()
    busform = BusinessForm()
    gurform = GuarantorForm()
    if request.method == 'POST':
        custform = CustomerForm(request.POST, request.FILES)
        busform = BusinessForm(request.POST)
        gurform = GuarantorForm(request.POST)

        if custform.is_valid() and busform.is_valid() and gurform.is_valid():
            customer = custform.save()

            business = busform.save(commit=False)
            business.customer = customer
            business.save()

            guarantor = gurform.save(commit=False)
            guarantor.customer = customer
            guarantor.save()

            loanNo = random.randrange(10000, 20000)
            amount = busform.cleaned_data.get('LoanAmount')
            loan = Loan(LoanNumber=loanNo, customer=customer, Amount=amount, officer=request.user.username)
            loan.save()

            sweetify.success(request, title=f'Loan {loan.LoanNumber} for {customer.fullname} successfully created ',
                             icon="success")
            return redirect('home')
        elif custform.errors:
            errors = dict(custform.errors)

            for key, value in errors.items():
                value = (value[0])

            sweetify.error(request, title=f'{key}', text=f"{value}", icon="error")
        elif busform.errors:
            errors = dict(busform.errors)

            for key, value in errors.items():
                value = (value[0])

            sweetify.error(request, title=f'{key}', text=f"{value}", icon="error")
        else:
            errors = dict(gurform.errors)

            for key, value in errors.items():
                value = (value[0])

            sweetify.error(request, title=f'{key}', text=f"{value}", icon="error")

    context = {"custform": custform, "gurform": gurform, "busform": busform}

    return render(request, 'loanapp/loanapplicationform.html', context)


@login_required(login_url='register')
def customerinformation(request, pk):
    customer = Customer.objects.get(id=pk)

    context = {'customer': customer}

    return render(request, 'loanapp/customerinformation.html', context)


@login_required(login_url='register')
@allowed_users(['officer'])
def updatecustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    business = customer.business_set.first()
    guarantor = customer.guarantor_set.first()
    loan = customer.loan_set.first()

    custform = CustomerForm(instance=customer)
    busform = BusinessForm(instance=business)
    gurform = GuarantorForm(instance=guarantor)

    if request.method == 'POST':
        custform = CustomerForm(request.POST, request.FILES, instance=customer)
        busform = BusinessForm(request.POST, instance=business)
        gurform = GuarantorForm(request.POST, instance=guarantor)

        if custform.is_valid() and custform.has_changed():
            custform.save()
            changes = custform.changed_data
            sweetify.success(request,
                             title=f'{customer.fullname} {changes[0]} was succesfully updated ',
                             icon="success")
            return redirect('all_customers')
        elif busform.is_valid() and busform.has_changed():
            status = loan.status
            if status != "Pending" and "LoanAmount" in busform.changed_data:
                sweetify.error(request,
                               title=f'{customer.fullname} Loan is already {status} and cant be altered ',
                               icon="error")
            else:
                busform.save()
                changes = busform.changed_data
                sweetify.success(request,
                                 title=f'{customer.fullname} {changes[0]} was succesfully updated ',
                                 icon="success")

            return redirect('all_customers')
        elif gurform.is_valid() and gurform.is_valid():

            gurform.save()
            changes = gurform.changed_data
            sweetify.success(request,
                             title=f'{customer.fullname} {changes[0]} was succesfully updated ',
                             icon="success")
            return redirect('all_customers')
        else:
            sweetify.error(request, title='something went wrong!!!', icon="error")

    context = {"custform": custform, "gurform": gurform, "busform": busform}

    return render(request, 'loanapp/loanapplicationform.html', context)


@login_required(login_url='register')
def loans(request):
    customers = Customer.objects.all().order_by('-id')

    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    pageobj = paginator.get_page(page_number)

    context = {'customers': customers, 'pages': pageobj}

    return render(request, 'loanapp/loantable.html', context)


@login_required(login_url='register')
def customerlist(request):
    customers = Customer.objects.all().order_by('-id')

    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    pageobj = paginator.get_page(page_number)

    context = {'customers': customers, 'pages': pageobj}

    return render(request, 'loanapp/customertable.html', context)


@login_required(login_url='register')
def paymentlist(request):
    payments = Payment.objects.all().order_by('-DatePaid')

    paginator = Paginator(payments, 10)
    page_number = request.GET.get('page')
    pageobj = paginator.get_page(page_number)

    context = {'payments': payments, 'pages': pageobj}

    return render(request, 'loanapp/paymenttable.html', context)


@login_required(login_url='register')
@allowed_users(['supervisor'])
def loanapproval(request):
    data = json.loads(request.body)

    action = data["action"]
    remarks = data["text"]
    cust = data["customer"]

    customer = Customer.objects.get(id=cust)
    loan = Loan.objects.get(customer=customer)
    loan.supervisor = request.user.username

    if action == "approve":
        loan.status = "Approved"
        if remarks:
            loan.Remark = remarks
        sweetify.success(request, title='Success', text='Loan Approved', icon='success')
    elif action == "reject":
        loan.status = "Denied"
        loan.Remark = remarks
        sweetify.success(request, title='Success', text='Loan Rejected', icon='success')

    loan.save()

    return JsonResponse("loan approved", safe=False)


@login_required(login_url='register')
def search(request):
    if request.method == "POST":

        data = json.loads(request.body)

        search = data.get('term')

        results = Customer.objects.filter(FirstName__icontains=search).values()

        if results:
            return JsonResponse(list(results), safe=False)
        else:
            sweetify.error(request, title='Error', text='Customer not found', icon='Error')
            return JsonResponse([], safe=False)


@login_required(login_url='register')
def settings(request):
    return render(request, 'loanapp/settings.html')


@login_required(login_url='register')
def customerinfopdf(request, pk):
    customer = Customer.objects.get(id=pk)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    c.setTitle(customer.fullname)

    text_obj = c.beginText(200, 170)
    # text_obj.setTextOrigin(inch, inch)
    text_obj.setFont("Times-Bold", 16)

    lines = []

    lines.append(customer.fullname)
    lines.append(str(customer.Dob))
    lines.append(customer.Email)
    lines.append(str(customer.Id_Passport))
    lines.append(customer.Gender)
    lines.append(str(customer.loan_set.first().LoanNumber))
    lines.append(str(customer.loan_set.first().Amount))
    lines.append(str(customer.payment_set.first().balance))

    for line in lines:
        text_obj.textLine(line)

    c.drawCentredString(270, 100, 'CUSTOMER INFORMATION')
    c.line(200, 110, 350, 110)
    c.drawText(text_obj)
    c.showPage()
    c.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="example.pdf")


@login_required(login_url='register')
def statusgraph(request):
    labels = []
    values = []

    loans = Loan.objects.values('status').annotate(status_count=Count('status'))
    for loan in loans:
        labels.append(loan['status'])
        values.append(loan['status_count'])

    data = {'labels': labels, 'data': values}

    return JsonResponse(data)

@login_required(login_url='register')
def businesstypegraph(request):
    labels = []
    values = []

    bustypes = Business.objects.values('BusinessType').annotate(type_count=Count('BusinessType'))
    for type in bustypes:
        labels.append(type['BusinessType'])
        values.append(type['type_count'])

    data = {'labels': labels, 'data': values}

    return JsonResponse(data)

def payment(request):
    data = json.loads(request.body)

    name = data["name"]
    phone = data["phone"]
    amount = data["amount"]
    fee = data["type"]

    customer = Customer.objects.get(Phone=phone)
    loan = customer.loan_set.first()
    payment = customer.payment_set.first()

    if payment:
        original = payment.Amount
        payment.Amount = original + int(amount)
    else:
        payment = Payment.objects.create(customer=customer, loan=loan, Amount=amount, Status="Timely")

    if fee == "Processing Fee":
        payment.Type = "Processing Fee"
    elif fee == "First Instalment":
        payment.Type = "First Instalment"
    elif fee == "Second Instalment":
        payment.Type = "Second Instalment"
    else:
        payment.Type = "Penalty"
    if int(amount) > loan.Amount:
        sweetify.warning(title='Overpay', text='Payment more that balance', icon='warning')
    payment.save()

    sweetify.success(request, title="Success", text="Payment made Successful")

    return JsonResponse('Data successfull sent', safe=False)


def paymentform(request):
    return render(request, 'loanapp/paymentform.html')


@login_required(login_url='register')
@allowed_users('administrator')
def disburse(request, pk):
    customer = Customer.objects.get(id=pk)
    loan = customer.loan_set.first()

    loan.status = "Disbursed"

    loan.save()

    sweetify.success(request, title="Success", text=f"Loan Successfully Disbursed to {customer.fullname} ")

    return redirect('home')
