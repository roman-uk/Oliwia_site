# Generated by Django 3.2 on 2021-06-19 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0015_alter_photoportfolio_seat_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoportfolio',
            name='photo_theme',
            field=models.ForeignKey(blank=True, default=False, help_text='Morze być puste', on_delete=django.db.models.deletion.DO_NOTHING, to='photographer.phototheme'),
            preserve_default=False,
        ),
    ]