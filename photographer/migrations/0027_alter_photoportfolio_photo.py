# Generated by Django 3.2 on 2021-06-19 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0026_alter_photoportfolio_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photoportfolio',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='reusable_photo'),
        ),
    ]
