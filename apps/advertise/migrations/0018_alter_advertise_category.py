# Generated by Django 4.1.4 on 2023-04-08 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0017_alter_advertise_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertise',
            name='category',
            field=models.CharField(choices=[['elektronika', 'elektronika'], ['maishiy', 'maishiy']], max_length=100),
        ),
    ]
