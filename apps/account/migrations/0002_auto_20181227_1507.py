# Generated by Django 2.0.8 on 2018-12-27 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('filer', '0001_initial'),
        #('auth', '0010_group_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_userprofile_avatar', to='filer.File'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='teamprofile',
            name='photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_teamprofile_avatar', to='filer.File'),
        ),
        migrations.AddField(
            model_name='teamprofile',
            name='team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.Team'),
        ),
        migrations.AddField(
            model_name='team',
            name='holder',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Holder'),
        ),
        migrations.AddField(
            model_name='team',
            name='perms',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions by object.', related_name='account_team_related', related_query_name='account_teams', to='account.Perm', verbose_name='object permissions'),
        ),
        migrations.AddField(
            model_name='team',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='perm',
            name='holder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Holder', verbose_name='holder'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='holder',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Holder'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='perm',
            unique_together={('holder', 'perm_label')},
        ),
    ]
