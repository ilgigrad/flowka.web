# Generated by Django 2.0.8 on 2019-02-08 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_auto_20190206_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey2019',
            name='type',
            field=models.IntegerField(choices=[(0, ''), (1, 'self employed'), (2, 'local administration'), (3, 'government'), (4, 'education'), (5, 'enterprise'), (6, 'non-profit, non governmental organisation'), (7, 'small or medium business'), (8, 'start-up'), (99, 'other...')], default=0, verbose_name='company type'),
        ),
        migrations.AddField(
            model_name='survey2019',
            name='type_other',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="specify the company's type"),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='activity',
            field=models.IntegerField(choices=[(0, ''), (1, 'wholesale distribution and retail trade'), (2, 'IT, digital, software, internet and telecom'), (3, 'bank, insurance or financial activities'), (4, 'industry and manufacturing'), (5, 'transportation, storage and logistic'), (6, 'construction, building, real estate'), (7, 'computers and electronics'), (8, 'research, science, environment'), (9, 'energy, electricity, gas, steam, water supply...'), (10, 'agriculture, forestry, fishing, mining'), (11, 'legal, law'), (12, 'professional services'), (13, 'information, media, communication'), (14, 'cinema, arts, entertainment and gaming'), (15, 'sport, recreation, outdoor'), (16, 'travel, hospitality, accomodation, restaurant, food activities'), (17, 'healthcare and social work activities'), (18, 'education'), (19, 'public administration, government'), (20, 'non-profit organisation'), (99, 'other...')], default=0, verbose_name='company activity'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='activity_other',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="specify the company's activity"),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='anomaly',
            field=models.IntegerField(choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='anomaly detection ?'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='classif',
            field=models.IntegerField(choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='classification, automated categories assignment'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='correl',
            field=models.IntegerField(choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='finding correlation among your data, causality or links between events'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='frequency',
            field=models.IntegerField(choices=[(0, ''), (200, 'daily'), (130, 'two or three times a week'), (50, 'weekly'), (30, 'two or three times a month'), (12, 'monthly'), (6, 'rarely'), (1, 'never')], default=0, verbose_name='analysis frequency'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='lines',
            field=models.IntegerField(verbose_name='average number of lines in a reports'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='pict',
            field=models.IntegerField(choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='picture categorization'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='predict',
            field=models.IntegerField(choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='predicting results'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='reports',
            field=models.IntegerField(verbose_name='average number of distinct reports are you browsing'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='revenue',
            field=models.IntegerField(choices=[(0, ''), (1, 'less than €1 Million'), (10, '€1 Million to 10€ Million'), (100, '€10 Million to 100€ Million'), (500, '€100 Million to 500€ Million'), (1000, '€500 Million to 1€ Billion'), (5000, 'over 1€ Billion')], default=0, verbose_name='company annual revenue'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='role',
            field=models.IntegerField(choices=[(0, ''), (1, 'liberal, partner, self employed'), (2, 'financial, accounting'), (3, 'IT/telecom'), (4, 'marketing, communication'), (5, 'sales'), (6, 'storage, logistic, supply-chain, transportation'), (7, 'human ressources'), (8, 'consultant, advisor'), (9, 'research, science academic'), (10, 'health, medical'), (11, 'journalist, media analyst'), (12, 'business executive, management, upper management'), (13, 'education'), (14, 'legal'), (15, 'buying, sourcing'), (16, 'technical, production'), (17, 'administration'), (18, 'developer, engineer'), (19, 'support services'), (20, 'entrepreneur'), (21, 'student'), (99, 'other...')], default=0, verbose_name='employee role'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='segment',
            field=models.IntegerField(choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='segmentation, building relevant groups among your data'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='test1',
            field=models.IntegerField(choices=[(0, "I don't know"), (1, 'response 1.'), (2, 'response 2.'), (3, 'response 3.')], default=1, verbose_name='test1'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='test2',
            field=models.IntegerField(choices=[(0, "I don't know"), (1, 'response 1.'), (2, 'response 2.'), (3, 'response 3.')], default=1, verbose_name='test2'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='test3',
            field=models.IntegerField(choices=[(0, "I don't know"), (1, 'response 1.'), (2, 'response 2.'), (3, 'response 3.')], default=1, verbose_name='test3'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='test4',
            field=models.IntegerField(choices=[(0, "I don't know"), (1, 'response 1.'), (2, 'response 2.'), (3, 'response 3.')], default=1, verbose_name='test4'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='text',
            field=models.IntegerField(choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'yes, very much'), (4, 'excellent')], default=0, verbose_name='text categorization'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='tool',
            field=models.IntegerField(choices=[(0, ''), (1, "I don't know"), (2, 'none, a pocket calculator or pencil, rubber and paper...'), (3, 'Spreadsheet, Microsoft Excel, Google Sheets, Open Office Calc'), (4, 'Business Intelligence Desktop tools, Tableau, Qlik Sense, Sisense, Looker...'), (5, 'Business Intelligence enterprise reporting tools, SAP Business Objects, IBM Cognos, Microsoft Analysis Services/Power BI '), (6, 'mainframe reports'), (7, 'developper tools, Python, Java, C#...'), (8, 'none of this...')], default=0, verbose_name='reporting tool'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='visualization',
            field=models.IntegerField(choices=[(0, ''), (1, "I don't know"), (2, 'raw listings'), (3, 'columns tables'), (4, 'pivot tables'), (5, 'Olap hypercubes'), (6, 'graphs, curves or charts')], default=0, verbose_name='visualization style of the reporting'),
        ),
    ]