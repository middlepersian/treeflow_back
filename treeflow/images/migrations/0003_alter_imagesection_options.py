# Generated by Django 4.1.4 on 2023-05-10 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_historicalimage_page_image_page'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagesection',
            options={'ordering': ['image', 'section']},
        ),
    ]
