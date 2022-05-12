# Generated by Django 3.1.13 on 2022-03-31 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0010_auto_20220331_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='comment_new_suggesiton',
        ),
        migrations.AddField(
            model_name='token',
            name='comment_new_suggestion',
            field=models.ManyToManyField(blank=True, related_name='token_comment_new_suggestion', to='corpus.CommentCategory'),
        ),
    ]