# Generated by Django 4.2.7 on 2024-03-14 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('images', '0005_remove_historicalimagesection_history_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_images', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
