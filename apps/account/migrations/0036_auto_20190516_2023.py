# Generated by Django 2.0.8 on 2019-05-16 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0035_auto_20190515_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holder',
            name='uiid',
            field=models.CharField(default='897b30ed', editable=False, max_length=8),
        ),
    ]