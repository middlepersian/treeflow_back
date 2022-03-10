# Generated by Django 3.1.13 on 2022-03-09 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0002_auto_20220309_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='previous',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next', to='corpus.token'),
        ),
    ]
