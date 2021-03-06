# Generated by Django 4.0.3 on 2022-04-11 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoanApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='BusinessType',
            field=models.CharField(choices=[('Micro Enterprise', 'MicroEnterprise'), ('Small Enterprise', 'SmallEnterprise'), ('Medium Enterprise', 'MediumEnterprise'), ('Macro Enterprise', 'MacroEnterprise')], max_length=500, verbose_name='Business_Type'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='Gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, verbose_name='Gender'),
        ),
    ]
