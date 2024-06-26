# Generated by Django 2.0.8 on 2019-02-14 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0014_auto_20190213_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey2019',
            name='is_autonomous',
        ),
        migrations.AddField(
            model_name='survey2019',
            name='is_analyst',
            field=models.BooleanField(default=False, help_text='Do you dive in your data to have a better understanding of underlying issues <br>rather than tracking the evolution of variables thru time', verbose_name='Do you analyze your data?'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='categories',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='columns',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='has_mathematic',
            field=models.BooleanField(default=False, help_text='Do you have some knowledge of mathematics or statistics that allow you to make advanced analysis of your data ?', verbose_name='Do you have some mathematical background ?'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='has_scientist',
            field=models.BooleanField(default=False, help_text='Do you have any data scientist or any dedicated team, easily approachable, in your working environment, with whom any Analysis question will have its answer in a few hours ? ', verbose_name='Are you close from data analyst ?'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='is_dependant',
            field=models.BooleanField(default=False, help_text='Check if you feel highly dependant from others to access new sets of data.<br>If you rely on someone else&#39;s work and need to make a request to another department (e.g. IT) , consultants or a partner company and wait for a while before getting datasets or reports ', verbose_name='Do you feel dependant ?'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='lines',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='records',
            field=models.IntegerField(choices=[(0, ''), (1, 'less than 1000'), (2, '1000 to 9,999 (thousand)'), (3, '10,000 to 99,999'), (4, '100,000 to 1 Million'), (5, '1 Million to 500 Million'), (6, 'over 500 Million')], default=0, help_text='What is the size of datasets on which reports rely on ?<br>e.g. a report that display informations over three weeks in 200 stores with an average of 50 sales a day,<br> ...the number of records will be 50 x 200 x 7 x 3 = 210,000', verbose_name='Average number of records'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='reports',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='revenue',
            field=models.IntegerField(choices=[(0, ''), (1, 'less than €1 Million'), (2, '€1 Million to €10 Million'), (3, '€10 Million to €100 Million'), (4, '€100 Million to €500 Million'), (5, '€500 Million to €1 Billion'), (6, 'over 1€ Billion')], default=0, help_text='Select the average annual revenue of your company. Leave empty if not allowed', verbose_name='company annual revenue'),
        ),
    ]
