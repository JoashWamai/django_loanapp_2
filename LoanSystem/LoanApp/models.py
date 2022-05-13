from django.db import models
from datetime import date,timedelta
from django.core.validators import MinValueValidator



class Customer(models.Model):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    FirstName = models.CharField(max_length=500, verbose_name="FirstName")
    LastName = models.CharField(max_length=500, verbose_name="LastName")
    Gender = models.CharField(max_length=10, choices=GENDER, verbose_name='Gender')
    Id_Passport = models.IntegerField(verbose_name="Id/Passport")
    Phone = models.IntegerField(verbose_name="Phone")
    Email = models.EmailField(verbose_name="Email", null=True, blank=True)
    Dob = models.DateField(verbose_name="Dob")
    Picture = models.ImageField(default='avatar.jpg', upload_to="UserImages/", null=True, blank=True)
    County = models.CharField(max_length=500, verbose_name="County")
    SubCounty = models.CharField(max_length=500, verbose_name="SubCounty")
    District = models.CharField(max_length=500, verbose_name="District")
    Location = models.CharField(max_length=500, verbose_name="Location")

    @property
    def fullname(self):
        return f'{self.FirstName} {self.LastName}'

    @property
    def age(self):
        today = date.today()
        age = today.year - self.Dob.year - ((today.month, today.day) < (self.Dob.month, self.Dob.day))
        return age

    def __str__(self):
        return f'{self.FirstName} {self.LastName}'


class Loan(models.Model):
    STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
        ('Paid', 'Paid'),
        ('Defaulted', 'Defaulted'),
        ('Disbursed', 'Disbursed')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    LoanNumber = models.IntegerField(verbose_name="Loan Number", unique=True)
    Amount = models.IntegerField(verbose_name="Loan Amount", validators=[MinValueValidator(7000)])
    DateCreated = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS, verbose_name="Loan Status", default="Pending")
    officer = models.CharField(max_length=255, verbose_name="Field_Officer", null=True)
    supervisor = models.CharField(max_length=255, verbose_name="Supervisor", null=True)
    Remark = models.CharField(max_length=255, verbose_name="Remark", default="Approved")

    @property
    def totalPayeble(self):
        interest = int((self.Amount * 3 / 100) * 2)

        return self.Amount + interest

    @property
    def instalment(self):
        return self.totalPayeble / 2

    @property
    def firstinstalmentdate(self):
        time_diff = timedelta(days=30)

        return self.DateCreated + time_diff

    @property
    def secondinstalmentdate(self):
        time_diff = timedelta(days=60)

        return self.DateCreated + time_diff

    def __str__(self):
        return f'{self.customer.fullname} - {self.LoanNumber}'


class Business(models.Model):
    TYPES = [
        ('Micro Enterprise', 'MicroEnterprise'),
        ('Small Enterprise', 'SmallEnterprise'),
        ('Medium Enterprise', 'MediumEnterprise'),
        ('Macro Enterprise', 'MacroEnterprise'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="customer")
    BusinessName = models.CharField(max_length=500, verbose_name="Business_Name")
    OperatingYears = models.IntegerField(verbose_name="OperatingYears")
    BusinessType = models.CharField(max_length=500, choices=TYPES, verbose_name="Business_Type")
    MonthlyIncome = models.IntegerField(verbose_name="Monthly_Income")
    LoanAmount = models.IntegerField(verbose_name="Loan_Amount")
    BusCounty = models.CharField(max_length=500, verbose_name="Bus_County")
    BusSubCounty = models.CharField(max_length=500, verbose_name="Bus_SubCounty")
    BusDistrict = models.CharField(max_length=500, verbose_name="Bus_District")
    BusLocation = models.CharField(max_length=500, verbose_name="Bus_Location")

    def __str__(self):
        return f'{self.BusinessName} - {self.customer.fullname}'


class Guarantor(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="customer")
    GFirstName = models.CharField(max_length=500, verbose_name="Guarantor_FName")
    GLastName = models.CharField(max_length=500, verbose_name="Guarantor_LName")
    GTelephone = models.IntegerField(verbose_name="Guarantor_Telephone")
    GResidence = models.CharField(max_length=500, verbose_name="Guarantor_Residence")
    Relationship = models.CharField(max_length=100, verbose_name="Relationship")

    def __str__(self):
        return f'{self.GFirstName} {self.GLastName} - {self.customer.fullname}'

    @property
    def fullname(self):
        return f'{self.GFirstName} {self.GLastName}'


class Payment(models.Model):
    TYPE = [
        ('Processing Fee', 'Processing Fee'),
        ('First Instalment', 'First Instalment'),
        ("Second Instalment", "Second Instalment"),
        ("Penalty", "Penalty")
    ]
    STATUS = [
        ('Late', 'Late'),
        ('Timely', 'Timely')
    ]
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE, verbose_name="loan", null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='customer', null=True)
    Amount = models.IntegerField(verbose_name="Payment Amount")
    Type = models.CharField(max_length=200, choices=TYPE, verbose_name="Payment type")
    DatePaid = models.DateTimeField(auto_now_add=True, verbose_name="Date Paid")
    Status = models.CharField(max_length=255, choices=STATUS, verbose_name="Payment Status")

    def __str__(self):
        return f'{self.customer.fullname} - {self.loan.LoanNumber}'

    @property
    def balance(self):
        if self.TYPE == "Processing Fee":
            return self.loan.totalPayeble
        else:
            return self.loan.totalPayeble - int(self.Amount)
