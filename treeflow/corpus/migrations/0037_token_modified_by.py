# Generated by Django 4.2.7 on 2024-03-14 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('corpus', '0036_bibentry_created_by_bibentry_modified_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_tokens', to=settings.AUTH_USER_MODEL),
        ),
    ]
