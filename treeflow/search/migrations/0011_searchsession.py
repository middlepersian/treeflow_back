# Generated by Django 4.2.7 on 2023-12-14 20:18

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('search', '0010_alter_searchcriteria_distance_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('session_id', models.CharField(blank=True, max_length=255, null=True)),
                ('results', django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(default=uuid.uuid4), blank=True, null=True, size=None)),
                ('formset', models.ManyToManyField(blank=True, to='search.searchcriteria')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'session_id')},
            },
        ),
    ]