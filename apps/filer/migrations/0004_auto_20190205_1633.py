# Generated by Django 2.0.8 on 2019-02-05 15:33

from django.db import migrations
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0003_auto_20190121_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='subjects',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, autocomplete_initial=True, autocomplete_view='tag:tag_subject_autocomplete', force_lowercase=True, help_text='Enter a comma-separated tag string', initial='CRM, HR, IT, business, correlation, customers, learning, legal, production, retail, retail/sales, retail/stocks', max_count=15, to='tag.TagSubject', tree=True),
        ),
    ]