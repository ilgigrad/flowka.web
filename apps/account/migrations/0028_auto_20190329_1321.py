# Generated by Django 2.0.8 on 2019-03-29 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_auto_20190328_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holder',
            name='uiid',
            field=models.CharField(default='bbb236cb', editable=False, max_length=8),
        ),
    ]