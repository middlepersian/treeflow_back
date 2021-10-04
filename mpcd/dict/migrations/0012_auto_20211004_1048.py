# Generated by Django 3.1.13 on 2021-10-04 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0011_auto_20211004_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(choices=[('astr', 'astronomy'), ('bot', 'botany'), ('econom', 'economy'), ('geogr', 'geography'), ('legal', 'legal'), ('measure', 'measurement'), ('med', 'medicine'), ('myth', 'mythology'), ('philos', 'philosophy'), ('pol', 'politics'), ('purity', 'purity'), ('ritual', 'ritual'), ('theol', 'theology'), ('zool', 'zoology')], max_length=8, unique=True),
        ),
    ]
