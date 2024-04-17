# Generated by Django 2.0.8 on 2019-02-05 15:33

from django.db import migrations, models
import tagulous.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey2019',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='uploaded at')),
                ('enterprise_classification', models.CharField(choices=[('ener', 'Energy'), ('tran', 'Transportation or Logistic'), ('tele', 'IT/Telecom'), ('fash', 'Fashion Clothes Shoes'), ('heal', 'Health'), ('bank', 'Bank, Insurance or Financial Business'), ('indu', 'Industry and Manufacturing'), ('cons', 'Construction, Building'), ('admi', 'Administration'), ('scie', 'Research, Science'), ('medi', 'Media, Communication, Press '), ('cine', 'Cinema, Art, Entairtainment, '), ('educ', 'Education'), ('lega', 'Legal Law'), ('reta', 'retail, distribution and sales'), ('spor', 'sport, leisure, outdoor'), ('othe', 'Other')], default='bk', max_length=4, verbose_name='enterprise_classification')),
                ('enterprise_classification_other', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='other classification')),
                ('data_access', models.BooleanField(default=True, unique=True, verbose_name='using data')),
                ('employee_activity', models.CharField(choices=[('fi', 'Financial'), ('ac', 'accountant'), ('it', 'IT/Telecom'), ('mk', 'Marketing Communication'), ('sa', 'Sales'), ('lo', 'Logistic, Supply-Chain, Transportation'), ('hr', 'Human Ressources'), ('co', 'Consulting, Audit'), ('re', 'Research, Science, Lab'), ('he', 'Health'), ('jo', 'Journalism'), ('ma', 'Management'), ('ed', 'Education'), ('le', 'Legal'), ('bu', 'Buying'), ('ad', 'Administration'), ('ot', 'Other')], default='ad', max_length=2, verbose_name='employee activity')),
                ('enterprise_activity_other', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='other activity')),
                ('analysis_frequency', models.IntegerField(blank=True, choices=[(200, 'daily'), (130, 'two or three times a week'), (50, 'weekly'), (30, 'two or three times a month'), (12, 'monthly'), (6, 'rarely'), (0, 'never')], default=30, verbose_name='analysis frequency')),
                ('reporting_style', models.IntegerField(blank=True, choices=[(0, "I don't know"), (3, 'pivot tables'), (2, 'columns tables'), (5, 'graphs'), (1, 'raw listings'), (4, 'Olap hypercubes')], default=30, verbose_name='reporting style')),
                ('reporting_tool', models.IntegerField(blank=True, choices=[(0, "I don't know"), (1, 'Spreadsheet, Microsoft Excel, Google Sheets, Open Office Calc'), (3, 'Business Intelligence enterprise reporting tools, SAP Business Objects, IBM Cognos, Microsoft Analysis Services/Power BI '), (2, 'Business Intelligence Desktop tools, Tableau, Qlik Sense, Sisense, Looker...'), (4, 'developper tools, Python, Java, C#...')], default=1, verbose_name='reporting tool')),
                ('extraction', models.BooleanField(default=False, verbose_name='extraction')),
                ('reports', models.IntegerField(blank=True, default=1, verbose_name='average number reports')),
                ('columns', models.IntegerField(blank=True, default=5, verbose_name='average number columns')),
                ('lines', models.IntegerField(blank=True, default=50, verbose_name='average number lines')),
                ('autonomy', models.BooleanField(default=False, verbose_name='autonomy')),
                ('dependant', models.BooleanField(default=False, verbose_name='feel dependant')),
                ('scientific', models.BooleanField(default=False, verbose_name='scientific')),
                ('data_science', models.BooleanField(default=False, verbose_name='data_scientist')),
                ('anomaly', models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'Yes very much')], default=1, verbose_name='anomaly')),
                ('classification', models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'Yes very much')], default=1, verbose_name='classification')),
                ('prediction', models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'Yes very much')], default=1, verbose_name='prediction')),
                ('correlation', models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'Yes very much')], default=1, verbose_name='correlation')),
                ('segmentation', models.IntegerField(blank=True, choices=[(0, 'not at all'), (1, 'not so much '), (2, 'yes '), (3, 'Yes very much')], default=1, verbose_name='segmentation')),
                ('test1', models.IntegerField(blank=True, choices=[(0, 'no idea'), (1, '1.'), (2, '2.'), (3, '2.')], default=1, verbose_name='test1')),
                ('test2', models.IntegerField(blank=True, choices=[(0, 'no idea'), (1, '1.'), (2, '2.'), (3, '2.')], default=1, verbose_name='test2')),
                ('test3', models.IntegerField(blank=True, choices=[(0, 'no idea'), (1, '1.'), (2, '2.'), (3, '2.')], default=1, verbose_name='test3')),
                ('test4', models.IntegerField(blank=True, choices=[(0, 'no idea'), (1, '1.'), (2, '2.'), (3, '2.')], default=1, verbose_name='test4')),
                ('firm_size', models.IntegerField(blank=True, choices=[(0, "I can't say"), (10, 'less than 10'), (50, '10 to 50.'), (200, '50 to 200.'), (1000, '200 to 1000'), (5000, 'over 1000')], default=10, verbose_name='firm Size')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('keys', tagulous.models.fields.TagField(_set_tag_meta=True, autocomplete_initial=True, autocomplete_view='tag:tag_subject_autocomplete', force_lowercase=True, help_text='Enter a comma-separated tag string', initial='CRM, HR, IT, business, correlation, customers, learning, legal, production, retail, retail/sales, retail/stocks', max_count=15, to='tag.TagSubject', tree=True)),
            ],
        ),
    ]
