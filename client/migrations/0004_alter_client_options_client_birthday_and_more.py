# Generated by Django 4.0.3 on 2022-03-13 17:29

import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_remove_client_groups_remove_client_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={},
        ),
        migrations.AddField(
            model_name='client',
            name='birthday',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=django.contrib.postgres.fields.citext.CIEmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='client',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]