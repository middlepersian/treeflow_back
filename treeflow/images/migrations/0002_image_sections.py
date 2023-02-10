# Generated by Django 4.1.4 on 2023-02-10 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0003_alter_dependency_rel_alter_historicaldependency_rel'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='sections',
            field=models.ManyToManyField(related_name='image_sections', to='corpus.section'),
        ),
    ]
