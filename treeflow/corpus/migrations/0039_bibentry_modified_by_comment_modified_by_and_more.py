# Generated by Django 4.2.7 on 2024-03-14 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('corpus', '0038_alter_token_modified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='bibentry',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_bib_entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dependency',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_dependencies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feature',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_features', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pos',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_pos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='section',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_sections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='source',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_sources', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='text',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_texts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bibentry',
            name='modified_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='modified_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='dependency',
            name='modified_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='feature',
            name='modified_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='pos',
            name='modified_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='section',
            name='modified_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='source',
            name='modified_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='text',
            name='modified_at',
            field=models.DateTimeField(),
        ),
    ]
