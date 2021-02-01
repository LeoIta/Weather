# Generated by Django 3.1.3 on 2021-02-01 20:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_city_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('name', 'user')},
        ),
    ]
