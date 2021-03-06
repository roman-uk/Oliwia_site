# Generated by Django 3.2 on 2021-06-19 05:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0012_contactdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdata',
            name='facebook_name',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='contactdata',
            name='instagram_name',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='descriptionreusable',
            name='content',
            field=models.TextField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='descriptionreusable',
            name='title',
            field=models.CharField(blank=True, default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photoportfolio',
            name='photo_theme',
            field=models.ForeignKey(blank=True, default='', help_text='Morze być puste', on_delete=django.db.models.deletion.SET_DEFAULT, to='photographer.phototheme'),
        ),
        migrations.AlterField(
            model_name='photoportfolio',
            name='seat_number',
            field=models.CharField(default='1', max_length=40),
        ),
    ]
