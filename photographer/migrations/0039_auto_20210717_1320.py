# Generated by Django 3.2 on 2021-07-17 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0038_rename_contactmessage_contactemail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactemail',
            name='password',
        ),
        migrations.RemoveField(
            model_name='contactemail',
            name='server',
        ),
    ]
