# Generated by Django 3.1.3 on 2021-02-03 17:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='name',
            new_name='cityId',
        ),
        migrations.AddField(
            model_name='city',
            name='cityName',
            field=models.CharField(default='Conversano', max_length=85),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.CharField(default='Italy', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='countryId',
            field=models.CharField(default='IT', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='urlPath',
            field=models.CharField(default='ttt', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('cityId', 'user')},
        ),
    ]