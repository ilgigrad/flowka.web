# Generated by Django 2.0.8 on 2019-01-08 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0002_auto_20190108_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snippet', models.TextField(blank=True, null=True)),
                ('metadata', models.TextField(blank=True, null=True)),
                ('transform', models.TextField(blank=True, null=True)),
                ('datafile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='filer.File', verbose_name='datafile')),
            ],
        ),
    ]
