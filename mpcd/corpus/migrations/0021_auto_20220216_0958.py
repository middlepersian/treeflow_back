# Generated by Django 3.1.13 on 2022-02-16 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0020_auto_20220216_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codexpart',
            name='part_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='historicalcodexpart',
            name='part_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]