# Generated by Django 3.2 on 2021-05-03 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0003_phototheme_site_tab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phototheme',
            name='site_tab',
            field=models.CharField(choices=[('start', 'start'), ('portrety', 'portrety'), ('okolicznosciowe', 'okolicznosciowe'), ('rodzinne', 'rodzinne'), ('sensualne', 'sensualne'), ('wiecej', 'wiecej')], default='wiecej', max_length=20),
            preserve_default=False,
        ),
    ]
