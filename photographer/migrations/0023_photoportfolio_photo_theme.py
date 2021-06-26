# Generated by Django 3.2 on 2021-06-19 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0022_photoportfolio_column'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoportfolio',
            name='photo_theme',
            field=models.ForeignKey(blank=True, help_text='Morze być puste', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='photographer.phototheme'),
        ),
    ]
