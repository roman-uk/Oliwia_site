# Generated by Django 3.2 on 2021-07-16 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0036_auto_20210712_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('server', models.CharField(default='smtp.gmail.com: 587', max_length=50)),
            ],
        ),
    ]
