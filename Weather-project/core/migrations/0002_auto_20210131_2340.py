# Generated by Django 3.1.3 on 2021-01-31 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='description',
        ),
        migrations.RemoveField(
            model_name='city',
            name='feeling',
        ),
        migrations.RemoveField(
            model_name='city',
            name='temperature',
        ),
        migrations.RemoveField(
            model_name='city',
            name='wind',
        ),
    ]
