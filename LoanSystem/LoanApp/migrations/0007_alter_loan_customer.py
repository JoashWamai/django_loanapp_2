# Generated by Django 4.0.3 on 2022-04-12 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LoanApp', '0006_alter_customer_picture_alter_loan_loannumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='customer',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='LoanApp.customer'),
            preserve_default=False,
        ),
    ]
