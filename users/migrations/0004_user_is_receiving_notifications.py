# Generated by Django 3.1.12 on 2021-06-04 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210505_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_receiving_notifications',
            field=models.BooleanField(default=True, verbose_name='receive notifications'),
        ),
    ]
