# Generated by Django 2.0.8 on 2019-02-08 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20190208_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holder',
            name='uiid',
            field=models.CharField(default='72b25eb8', editable=False, max_length=8),
        ),
    ]