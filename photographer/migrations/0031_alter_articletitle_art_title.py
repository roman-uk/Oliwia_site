# Generated by Django 3.2 on 2021-07-05 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0030_alter_articlebody_art_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articletitle',
            name='art_title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
