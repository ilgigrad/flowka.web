# Generated by Django 2.0.8 on 2019-05-06 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0033_auto_20190501_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holder',
            name='uiid',
            field=models.CharField(default='09b26e59', editable=False, max_length=8),
        ),
    ]