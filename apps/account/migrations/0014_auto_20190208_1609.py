# Generated by Django 2.0.8 on 2019-02-08 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20190208_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holder',
            name='uiid',
            field=models.CharField(default='124abe86', editable=False, max_length=8),
        ),
    ]
