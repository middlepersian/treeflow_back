# Generated by Django 3.1.13 on 2022-03-31 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('corpus', '0009_auto_20220329_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(blank=True, choices=[('C', 'Transcription'), ('L', 'Transliteration'), ('S', 'Semantics'), ('M', 'Morphology'), ('X', 'Syntax')], max_length=8, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='historicaltoken',
            name='language',
            field=models.CharField(blank=True, choices=[('akk', 'Akkadian'), ('ara', 'Arabic'), ('arc', 'Imperial Aramaic (700-300 BCE), Official Aramaic (700-300 BCE)'), ('ave', 'Avestan'), ('eng', 'English'), ('deu', 'German'), ('guj', 'Gujarati'), ('fra', 'French'), ('grc', 'Ancient Greek (to 1453)'), ('ita', 'Italian'), ('pal', 'Pahlavi'), ('san', 'Sanskrit'), ('spa', 'Spanish'), ('xpr', 'Parthian')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='language',
            field=models.CharField(blank=True, choices=[('akk', 'Akkadian'), ('ara', 'Arabic'), ('arc', 'Imperial Aramaic (700-300 BCE), Official Aramaic (700-300 BCE)'), ('ave', 'Avestan'), ('eng', 'English'), ('deu', 'German'), ('guj', 'Gujarati'), ('fra', 'French'), ('grc', 'Ancient Greek (to 1453)'), ('ita', 'Italian'), ('pal', 'Pahlavi'), ('san', 'Sanskrit'), ('spa', 'Spanish'), ('xpr', 'Parthian')], max_length=3, null=True),
        ),
        migrations.CreateModel(
            name='HistoricalCommentCategory',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('category', models.CharField(blank=True, choices=[('C', 'Transcription'), ('L', 'Transliteration'), ('S', 'Semantics'), ('M', 'Morphology'), ('X', 'Syntax')], max_length=8, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical comment category',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='token',
            name='comment_new_suggesiton',
            field=models.ManyToManyField(blank=True, related_name='token_comment_new_suggesiton', to='corpus.CommentCategory'),
        ),
        migrations.AddField(
            model_name='token',
            name='comment_to_discuss',
            field=models.ManyToManyField(blank=True, related_name='token_comment_to_discuss', to='corpus.CommentCategory'),
        ),
        migrations.AddField(
            model_name='token',
            name='comment_uncertain',
            field=models.ManyToManyField(blank=True, related_name='token_comment_uncertain', to='corpus.CommentCategory'),
        ),
    ]