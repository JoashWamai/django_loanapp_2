from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Business)
admin.site.register(Guarantor)
admin.site.register(Loan)

admin.site.register(Payment)

