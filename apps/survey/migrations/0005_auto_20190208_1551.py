# Generated by Django 2.0.8 on 2019-02-08 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20190208_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey2019',
            name='anomaly',
            field=models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='anomaly detection ?'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='classif',
            field=models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='classification, automated categories assignment'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='correl',
            field=models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='finding correlation among your data, causality or links between events'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='pict',
            field=models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='picture categorization'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='predict',
            field=models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='predicting results'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='revenue',
            field=models.IntegerField(choices=[(0, ''), (1, 'less than €1 Million'), (10, '€1 Million to €10 Million'), (100, '€10 Million to €100 Million'), (500, '€100 Million to €500 Million'), (1000, '€500 Million to €1 Billion'), (5000, 'over 1€ Billion')], default=0, verbose_name='company annual revenue'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='segment',
            field=models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='segmentation, building relevant groups among your data'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='test1',
            field=models.IntegerField(blank=True, choices=[(0, "I don't know"), (1, 'response 1.'), (2, 'response 2.'), (3, 'response 3.')], default=1, verbose_name='test1'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='test2',
            field=models.IntegerField(blank=True, choices=[(0, "I don't know"), (1, 'response 1.'), (2, 'response 2.'), (3, 'response 3.')], default=1, verbose_name='test2'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='test3',
            field=models.IntegerField(blank=True, choices=[(0, "I don't know"), (1, 'response 1.'), (2, 'response 2.'), (3, 'response 3.')], default=1, verbose_name='test3'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='test4',
            field=models.IntegerField(blank=True, choices=[(0, "I don't know"), (1, 'response 1.'), (2, 'response 2.'), (3, 'response 3.')], default=1, verbose_name='test4'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='text',
            field=models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='text categorization'),
        ),
    ]
