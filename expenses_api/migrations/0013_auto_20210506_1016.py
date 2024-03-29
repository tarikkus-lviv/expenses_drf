# Generated by Django 3.1.6 on 2021-05-06 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses_api', '0012_salary_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salary',
            name='salary',
        ),
        migrations.AddField(
            model_name='salary',
            name='end_salary',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='End salary'),
        ),
        migrations.AddField(
            model_name='salary',
            name='start_salary',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Start salary'),
        ),
        migrations.AddField(
            model_name='salary',
            name='total_salary',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Total salary'),
        ),
    ]
