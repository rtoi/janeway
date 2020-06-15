# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-06-11 15:54
from __future__ import unicode_literals

import core.file_system
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import repository.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('submission', '0043_auto_20200523_1158'),
        ('press', '0021_auto_20190329_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255)),
                ('affiliation', models.TextField(blank=True, null=True)),
                ('orcid', models.CharField(blank=True, max_length=255, null=True, verbose_name='ORCID')),
            ],
            options={
                'ordering': ('last_name',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('body', models.TextField(verbose_name='Write your comment:')),
                ('is_reviewed', models.BooleanField(default=False)),
                ('is_public', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_time', '-pk'),
            },
        ),
        migrations.CreateModel(
            name='Preprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(default='preprint_unsubmitted', max_length=25)),
                ('title', models.CharField(help_text='Your article title', max_length=300)),
                ('abstract', models.TextField(blank=True, help_text='Please avoid pasting content from word processors as they can add unwanted styling to the abstract. You can retype the abstract here or copy and paste it into notepad/a plain text editor before pasting here.', null=True)),
                ('meta_image', models.ImageField(blank=True, null=True, storage=core.file_system.JanewayFileSystemStorage(location='/home/ajrbyers/janeway/src/media'), upload_to=repository.models.preprint_file_upload)),
                ('comments_editor', models.TextField(blank=True, help_text="Add any comments you'd like the editor to consider here.", null=True, verbose_name='Comments to the Editor')),
                ('doi', models.CharField(blank=True, max_length=100, null=True)),
                ('preprint_decision_notification', models.BooleanField(default=False)),
                ('date_started', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_submitted', models.DateTimeField(blank=True, null=True)),
                ('date_accepted', models.DateTimeField(blank=True, null=True)),
                ('date_declined', models.DateTimeField(blank=True, null=True)),
                ('date_published', models.DateTimeField(blank=True, null=True)),
                ('date_updated', models.DateTimeField(blank=True, null=True)),
                ('current_step', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='PreprintAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessed', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PreprintAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Author')),
                ('preprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Preprint')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='PreprintFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=core.file_system.JanewayFileSystemStorage(location='files/'), upload_to=repository.models.preprint_file_upload)),
                ('original_filename', models.TextField()),
                ('uploaded', models.DateTimeField(default=django.utils.timezone.now)),
                ('mime_type', models.CharField(blank=True, max_length=255, null=True)),
                ('size', models.PositiveIntegerField(default=0)),
                ('preprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Preprint')),
            ],
        ),
        migrations.CreateModel(
            name='PreprintVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField(default=1)),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.PreprintFile')),
                ('preprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Preprint')),
            ],
            options={
                'ordering': ('-version', '-date_time', '-id'),
            },
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(default='www.example.com', max_length=255, unique=True)),
                ('is_secure', models.BooleanField(default=False, help_text='If the site should redirect to HTTPS, mark this.')),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=15)),
                ('object_name', models.CharField(help_text='eg. preprint or article', max_length=255)),
                ('object_name_plural', models.CharField(help_text='eg. preprints or articles', max_length=255)),
                ('logo', models.ImageField(blank=True, null=True, storage=core.file_system.JanewayFileSystemStorage(location='/home/ajrbyers/janeway/src/media'), upload_to=repository.models.repo_media_upload)),
                ('publisher', models.CharField(help_text='Used for outputs including DC and Citation metadata', max_length=255)),
                ('custom_js_code', models.TextField(blank=True, help_text='The contents of this field are output into the JS areaat the foot of every Repository page.', null=True)),
                ('live', models.BooleanField(default=False)),
                ('limit_upload_to_pdf', models.BooleanField(default=False, help_text='If set to True, this will require all file uploads fromauthors to be PDF files.')),
                ('about', models.TextField(blank=True, null=True)),
                ('start', models.TextField(blank=True, null=True)),
                ('submission', models.TextField(blank=True, null=True)),
                ('publication', models.TextField(blank=True, null=True)),
                ('decline', models.TextField(blank=True, null=True)),
                ('random_homepage_preprints', models.BooleanField(default=False)),
                ('homepage_preprints', models.ManyToManyField(blank=True, to='submission.Article')),
                ('managers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('press', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='press.Press')),
            ],
            options={
                'verbose_name_plural': 'repositories',
            },
        ),
        migrations.CreateModel(
            name='RepositoryField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('input_type', models.CharField(choices=[('text', 'Text'), ('select', 'Dropdown'), ('checkbox', 'Checkbox'), ('number', 'Number'), ('date', 'Date')], max_length=255)),
                ('choices', models.CharField(blank=True, help_text='Separate choices with the bar | character.', max_length=1000, null=True)),
                ('required', models.BooleanField(default=True)),
                ('order', models.IntegerField()),
                ('help_text', models.TextField(blank=True, null=True)),
                ('display', models.BooleanField(default=False, help_text='Whether or not display this field in the article page')),
                ('dc_metadata_type', models.CharField(help_text='If this field is to be output as a dc metadata field you can addthe type here.', max_length=255)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Repository')),
            ],
        ),
        migrations.CreateModel(
            name='RepositoryFieldAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.RepositoryField')),
                ('preprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Preprint')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True)),
                ('enabled', models.BooleanField(default=True, help_text='If disabled, this subject will not appear publicly.')),
                ('editors', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='repository.Subject')),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Repository')),
            ],
            options={
                'ordering': ('slug', 'pk'),
            },
        ),
        migrations.CreateModel(
            name='VersionQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_type', models.CharField(choices=[('correction', 'Correction'), ('version', 'New Version')], max_length=10)),
                ('date_submitted', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_decision', models.DateTimeField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.PreprintFile')),
                ('preprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Preprint')),
            ],
        ),
        migrations.AddField(
            model_name='preprintaccess',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.PreprintFile'),
        ),
        migrations.AddField(
            model_name='preprintaccess',
            name='preprint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Preprint'),
        ),
        migrations.AddField(
            model_name='preprint',
            name='curent_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='curent_version', to='repository.PreprintVersion'),
        ),
        migrations.AddField(
            model_name='preprint',
            name='keywords',
            field=models.ManyToManyField(blank=True, null=True, to='submission.Keyword'),
        ),
        migrations.AddField(
            model_name='preprint',
            name='license',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='submission.Licence'),
        ),
        migrations.AddField(
            model_name='preprint',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='preprint',
            name='repository',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.Repository'),
        ),
        migrations.AddField(
            model_name='preprint',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.Subject'),
        ),
        migrations.AddField(
            model_name='preprint',
            name='submission_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submission_file', to='repository.PreprintFile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='preprint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.Preprint'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.Comment'),
        ),
        migrations.AlterUniqueTogether(
            name='preprintauthor',
            unique_together=set([('author', 'preprint')]),
        ),
    ]
