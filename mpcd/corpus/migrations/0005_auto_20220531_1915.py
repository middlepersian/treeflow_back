# Generated by Django 3.1.13 on 2022-05-31 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0004_auto_20220530_1249'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='dependency',
            name='valid_rel',
        ),
        migrations.RemoveConstraint(
            model_name='dependency',
            name='head_rel',
        ),
        migrations.AddField(
            model_name='dependency',
            name='producer',
            field=models.IntegerField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='dependency',
            name='rel',
            field=models.CharField(max_length=9),
        ),
    ]
