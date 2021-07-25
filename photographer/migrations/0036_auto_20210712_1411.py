# Generated by Django 3.2 on 2021-07-12 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0035_alter_articlebody_art_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactdata',
            name='email',
        ),
        migrations.RemoveField(
            model_name='contactdata',
            name='facebook_link',
        ),
        migrations.RemoveField(
            model_name='contactdata',
            name='facebook_name',
        ),
        migrations.RemoveField(
            model_name='contactdata',
            name='instagram_link',
        ),
        migrations.RemoveField(
            model_name='contactdata',
            name='instagram_name',
        ),
        migrations.RemoveField(
            model_name='contactdata',
            name='telephone',
        ),
        migrations.AddField(
            model_name='contactdata',
            name='link_address',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contactdata',
            name='link_label',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AddField(
            model_name='contactdata',
            name='normal_label',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]