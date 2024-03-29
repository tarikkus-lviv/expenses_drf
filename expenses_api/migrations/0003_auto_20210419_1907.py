# Generated by Django 3.1.6 on 2021-04-19 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expenses_api', '0002_auto_20210419_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='expenses_api.category'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='salary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_salary', to='expenses_api.salary'),
        ),
    ]
