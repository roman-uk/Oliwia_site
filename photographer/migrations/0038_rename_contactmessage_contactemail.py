# Generated by Django 3.2 on 2021-07-16 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0037_contactmessage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContactMessage',
            new_name='ContactEmail',
        ),
    ]
