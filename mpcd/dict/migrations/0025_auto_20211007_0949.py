# Generated by Django 3.1.13 on 2021-10-07 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0024_auto_20211007_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='categories',
            field=models.ManyToManyField(blank=True, to='dict.Category'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='definitions',
            field=models.ManyToManyField(blank=True, to='dict.Definition'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='loanwords',
            field=models.ManyToManyField(blank=True, to='dict.LoanWord'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='references',
            field=models.ManyToManyField(blank=True, to='dict.Reference'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='translations',
            field=models.ManyToManyField(blank=True, to='dict.Translation'),
        ),
    ]