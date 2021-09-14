# Generated by Django 3.1.13 on 2021-09-14 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0002_auto_20210914_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltokencontainer',
            name='section',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='codex.section'),
        ),
        migrations.AddField(
            model_name='tokencontainer',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='codex.section'),
        ),
        migrations.AlterField(
            model_name='historicaltext',
            name='text_sigle',
            field=models.CharField(choices=[('DMX', 'DMX'), ('ENN', 'ENN')], max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='section_container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section', to='codex.section'),
        ),
        migrations.AlterField(
            model_name='text',
            name='text_sigle',
            field=models.CharField(choices=[('DMX', 'DMX'), ('ENN', 'ENN')], max_length=4, null=True),
        ),
    ]
