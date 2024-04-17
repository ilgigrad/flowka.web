from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacollect', '0002_auto_20190328_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='slug',
            field=models.CharField(blank=True, default='', help_text='slug', max_length=100, null=True, verbose_name='slug'),
        ),
    ]
