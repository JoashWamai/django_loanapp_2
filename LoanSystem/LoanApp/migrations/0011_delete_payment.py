# Generated by Django 4.0.3 on 2022-04-14 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LoanApp', '0010_payment_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
