# Generated by Django 2.0.8 on 2019-04-28 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0031_auto_20190410_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holder',
            name='uiid',
            field=models.CharField(default='886c71d1', editable=False, max_length=8),
        ),
    ]
