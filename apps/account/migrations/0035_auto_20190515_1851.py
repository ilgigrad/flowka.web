# Generated by Django 2.0.8 on 2019-05-15 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0034_auto_20190506_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holder',
            name='uiid',
            field=models.CharField(default='4db49cbb', editable=False, max_length=8),
        ),
    ]
