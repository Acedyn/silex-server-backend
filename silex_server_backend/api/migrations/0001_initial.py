# Generated by Django 3.2 on 2021-04-20 10:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('code', models.SlugField(default='untitled')),
                ('name', models.CharField(default='untitled', max_length=250)),
                ('root', models.CharField(max_length=250)),
                ('framerate', models.FloatField(default=25.0)),
                ('width', models.PositiveIntegerField(default=1920)),
                ('height', models.PositiveIntegerField(default=1080)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('index', models.PositiveIntegerField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sequences', to='api.project')),
            ],
            options={
                'unique_together': {('index', 'project')},
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('code', models.SlugField(default='untitled')),
                ('name', models.CharField(default='untitled', max_length=250)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='api.project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('index', models.PositiveIntegerField()),
                ('framerate', models.FloatField(default=25.0)),
                ('width', models.PositiveIntegerField(default=1920)),
                ('height', models.PositiveIntegerField(default=1080)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shots', to='api.project')),
                ('sequence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shots', to='api.sequence')),
            ],
            options={
                'unique_together': {('index', 'project', 'sequence')},
            },
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('index', models.PositiveIntegerField()),
                ('valid', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='api.project')),
                ('sequence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='api.sequence')),
                ('shot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='api.shot')),
            ],
            options={
                'unique_together': {('index', 'project', 'sequence', 'shot')},
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('code', models.SlugField(default='untitled')),
                ('name', models.CharField(default='untitled', max_length=250)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='api.project')),
            ],
            options={
                'unique_together': {('code', 'project')},
            },
        ),
    ]
