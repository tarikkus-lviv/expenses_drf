# Generated by Django 3.1.6 on 2021-04-19 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses_api', '0003_auto_20210419_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='salary',
        ),
    ]
