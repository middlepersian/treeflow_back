# Generated by Django 4.2.7 on 2024-03-14 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0039_bibentry_modified_by_comment_modified_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]