# Generated by Django 4.1.4 on 2023-04-08 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0013_category_alter_advertise_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]
