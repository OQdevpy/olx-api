# Generated by Django 4.1.4 on 2023-04-08 05:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0015_alter_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertise',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
