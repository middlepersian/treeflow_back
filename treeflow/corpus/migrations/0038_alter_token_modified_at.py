# Generated by Django 4.2.7 on 2024-03-14 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0037_token_modified_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='modified_at',
            field=models.DateTimeField(),
        ),
    ]
