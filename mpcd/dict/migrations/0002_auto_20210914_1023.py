# Generated by Django 3.1.13 on 2021-09-14 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='book',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='footnote',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='pages',
        ),
        migrations.AddField(
            model_name='reference',
            name='reference',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
