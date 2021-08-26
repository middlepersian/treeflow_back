# Generated by Django 3.1.13 on 2021-08-25 09:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('doi', models.URLField(null=True)),
                ('lemma', models.CharField(max_length=30, unique=True)),
                ('dict', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dict.dictionary')),
            ],
        ),
    ]