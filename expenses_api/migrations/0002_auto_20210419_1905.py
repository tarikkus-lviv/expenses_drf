# Generated by Django 3.1.6 on 2021-04-19 19:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('expenses_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.FloatField(blank=True, default=0, null=True, verbose_name='Salary')),
                ('salary_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Salary Date')),
            ],
            options={
                'verbose_name': 'Salary',
            },
        ),
        migrations.RemoveField(
            model_name='expense',
            name='salary_date',
        ),
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expense', to='expenses_api.category'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='salary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expense', to='expenses_api.salary'),
        ),
    ]