# Generated by Django 3.1 on 2020-09-26 09:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_description', models.CharField(max_length=200)),
                ('additional_comment', models.TextField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
    ]