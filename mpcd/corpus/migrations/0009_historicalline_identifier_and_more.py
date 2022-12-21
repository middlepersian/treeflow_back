# Generated by Django 4.1.4 on 2022-12-21 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0008_alter_token_line'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalline',
            name='identifier',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicalline',
            name='number_in_text',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='line',
            name='identifier',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='line',
            name='number_in_text',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
