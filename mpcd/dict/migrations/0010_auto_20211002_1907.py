# Generated by Django 3.1.13 on 2021-10-02 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0009_auto_20211002_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='dict',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='dict.dictionary'),
        ),
    ]
