# Generated by Django 3.1.13 on 2021-10-07 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0023_auto_20211007_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='loanwords',
            field=models.ManyToManyField(blank=True, related_name='enloan', to='dict.LoanWord'),
        ),
    ]