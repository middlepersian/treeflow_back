# Generated by Django 3.1.13 on 2022-02-14 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0015_auto_20220211_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalcodextoken',
            name='gloss',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicaltoken',
            name='gloss',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='gloss',
            field=models.TextField(blank=True, null=True),
        ),
    ]
