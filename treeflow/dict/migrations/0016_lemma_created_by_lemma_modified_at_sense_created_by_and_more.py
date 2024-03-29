# Generated by Django 4.2.7 on 2024-03-14 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dict', '0015_remove_historicallemma_history_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lemma',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_lemmas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lemma',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='sense',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_senses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sense',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
