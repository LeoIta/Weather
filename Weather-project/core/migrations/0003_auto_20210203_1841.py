# Generated by Django 3.1.3 on 2021-02-03 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210203_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.CharField(default='aa', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.CharField(max_length=50),
        ),
    ]