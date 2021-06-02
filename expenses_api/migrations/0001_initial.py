# Generated by Django 3.1.6 on 2021-04-19 14:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=256, null=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=256, null=True, verbose_name='Name')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Price')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
                ('salary', models.FloatField(blank=True, default=0, null=True, verbose_name='Salary')),
                ('salary_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Salary Date')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='expenses_api.category')),
            ],
            options={
                'verbose_name': 'Expense',
                'verbose_name_plural': 'Expenses',
            },
        ),
    ]
