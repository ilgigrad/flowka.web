# Generated by Django 2.0.8 on 2019-02-13 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0013_auto_20190212_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey2019',
            name='categories',
            field=models.IntegerField(default=0, help_text='categories are data that can not be easily computed. They are defined neither by floats nor integers. For exemple : geographic areas, colors or groups...', verbose_name='Average number of categories/dimensions'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='can_extract',
            field=models.BooleanField(default=False, help_text='Check if you use to export raw data out of the reporting tool to make analysis in a spreadsheets tool', verbose_name='Are you sometimes extracting data out of that tool ?'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='columns',
            field=models.IntegerField(default=5, help_text='What is the average number of columns or indicators contained in your reports ?', verbose_name='Average number of columns/indicators'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='frequency',
            field=models.IntegerField(choices=[(0, ''), (200, 'daily'), (130, 'two or three times a week'), (50, 'weekly'), (30, 'two or three times a month'), (12, 'monthly'), (6, 'rarely'), (1, 'never')], default=0, help_text='How often are you analysing or building reports on those data ?', verbose_name='analysis frequency'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='has_data',
            field=models.BooleanField(default=True, help_text='Check if your department is holding data (sales, logistic, clients, products details, technical data...)', verbose_name='Are you dealing with data ?'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='lines',
            field=models.IntegerField(default=0, help_text='What is the average number of lines contained in your reports ?', verbose_name='Average number of lines'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='records',
            field=models.IntegerField(default=0, help_text='largest size of datasets on which reports rely on ?', verbose_name='How many records ?'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='reports',
            field=models.IntegerField(default=0, help_text='What is the average number of distinct reports or charts are you usually browsing ?', verbose_name='Average number of reports'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='role',
            field=models.IntegerField(choices=[(0, ''), (1, 'liberal, partner, self employed'), (2, 'financial, accounting'), (3, 'IT/telecom'), (4, 'marketing, communication'), (5, 'sales'), (6, 'storage, logistic, supply-chain, transportation'), (7, 'human ressources'), (8, 'consultant, advisor'), (9, 'research, science academic'), (10, 'health, medical'), (11, 'journalist, media analyst'), (12, 'business executive, management, upper management'), (13, 'education'), (14, 'legal'), (15, 'buying, sourcing'), (16, 'technical, production'), (17, 'administration'), (18, 'developer, engineer'), (19, 'support services'), (20, 'entrepreneur'), (21, 'student'), (99, 'other...')], default=0, help_text='What is your occupation or the department in which you work ?', verbose_name='employee role'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='tool',
            field=models.IntegerField(choices=[(0, ''), (1, "I don't know"), (2, 'none, a pocket calculator or pencil, rubber and paper...'), (3, 'Spreadsheet, Microsoft Excel, Google Sheets, Open Office Calc'), (4, 'Business Intelligence Desktop tools, Tableau, Qlik Sense, Sisense, Looker...'), (5, 'Business Intelligence enterprise reporting tools, SAP Business Objects, IBM Cognos, Microsoft Analysis Services/Power BI '), (6, 'Enterprise Business Application or Package Software (SAP, PeopleSoft, Microsoft Dynamics, Cegid, Generix... )'), (7, "Web's software as a service solution"), (8, 'IT specific reports'), (9, 'AI analysis, IBM Watson, Microsoft Azur Machine Learning...'), (10, 'developper tools, Python, Java, C#...'), (11, 'none of this...')], default=0, help_text='What tool or software are you mainly using for building or looking at charts ?', verbose_name='reporting tool'),
        ),
        migrations.AlterField(
            model_name='survey2019',
            name='visualization',
            field=models.IntegerField(choices=[(0, ''), (1, "I don't know"), (2, 'raw listings'), (3, 'columns tables'), (4, 'pivot tables'), (5, 'Olap hypercubes'), (6, 'graphs, curves or charts')], default=0, help_text='How often are you analysing or building reports on those data ?', verbose_name='visualization style of the reporting'),
        ),
    ]
