# Generated by Django 4.1.4 on 2023-07-17 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_alter_imagesection_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['identifier', 'number']},
        ),
    ]