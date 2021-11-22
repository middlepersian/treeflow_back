# Generated by Django 3.1.13 on 2021-10-04 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0013_auto_20211004_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalentry',
            name='loanwords',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='loanwords',
        ),
        migrations.AddField(
            model_name='entry',
            name='loanwords',
            field=models.ManyToManyField(blank=True, null=True, to='dict.LoanWord'),
        ),
    ]