# Generated by Django 2.0.8 on 2019-02-08 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_auto_20190208_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey2019',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]
