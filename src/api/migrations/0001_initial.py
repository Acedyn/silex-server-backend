# Generated by Django 3.2 on 2021-04-30 18:58

import api.models
import api.validators
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('root', models.CharField(max_length=250, null=True, validators=[api.validators.path_validator])),
                ('state', models.CharField(max_length=10, validators=[api.validators.state_validator])),
                ('framerate', models.FloatField(default=25.0)),
                ('width', models.PositiveIntegerField(default=1920)),
                ('height', models.PositiveIntegerField(default=1080)),
                ('name', models.SlugField(default='untitled', unique=True)),
                ('label', models.CharField(default='untitled', max_length=50)),
                ('color', models.CharField(default=api.models.random_hexa_color, max_length=7, validators=[api.validators.color_validator])),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_projects', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_projects', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_projects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'unique_together': {('root',)},
            },
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('root', models.CharField(max_length=250, null=True, validators=[api.validators.path_validator])),
                ('state', models.CharField(max_length=10, validators=[api.validators.state_validator])),
                ('framerate', models.FloatField(default=25.0)),
                ('width', models.PositiveIntegerField(default=1920)),
                ('height', models.PositiveIntegerField(default=1080)),
                ('index', models.PositiveIntegerField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_sequences', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_sequences', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sequences', to='api.project')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_sequences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': [('add_any_entity', 'Can add entity that belong to a project the user does not own'), ('change_any_entity', 'Can change entity that belong to a project the user does not own'), ('delete_any_entity', 'Can delete entity that belong to a project the user does not own')],
                'unique_together': {('index', 'project'), ('project', 'root')},
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('root', models.CharField(max_length=250, null=True, validators=[api.validators.path_validator])),
                ('state', models.CharField(max_length=10, validators=[api.validators.state_validator])),
                ('framerate', models.FloatField(default=25.0)),
                ('width', models.PositiveIntegerField(default=1920)),
                ('height', models.PositiveIntegerField(default=1080)),
                ('name', models.SlugField(default='untitled')),
                ('label', models.CharField(default='untitled', max_length=250)),
                ('entity_id', models.PositiveIntegerField(null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_tasks', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_tasks', to=settings.AUTH_USER_MODEL)),
                ('entity_type', models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'api'), ('model', 'Sequence')), models.Q(('app_label', 'api'), ('model', 'Shot')), models.Q(('app_label', 'api'), ('model', 'Asset')), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='api.project')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('root', models.CharField(max_length=250, null=True, validators=[api.validators.path_validator])),
                ('state', models.CharField(max_length=10, validators=[api.validators.state_validator])),
                ('framerate', models.FloatField(default=25.0)),
                ('width', models.PositiveIntegerField(default=1920)),
                ('height', models.PositiveIntegerField(default=1080)),
                ('index', models.PositiveIntegerField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_shots', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_shots', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shots', to='api.project')),
                ('sequence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shots', to='api.sequence')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_shots', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': [('add_any_entity', 'Can add entity that belong to a project the user does not own'), ('change_any_entity', 'Can change entity that belong to a project the user does not own'), ('delete_any_entity', 'Can delete entity that belong to a project the user does not own')],
                'unique_together': {('project', 'sequence', 'root'), ('index', 'project', 'sequence')},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='projects',
            field=models.ManyToManyField(to='api.Project'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('root', models.CharField(max_length=250, null=True, validators=[api.validators.path_validator])),
                ('state', models.CharField(max_length=10, validators=[api.validators.state_validator])),
                ('framerate', models.FloatField(default=25.0)),
                ('width', models.PositiveIntegerField(default=1920)),
                ('height', models.PositiveIntegerField(default=1080)),
                ('index', models.PositiveIntegerField()),
                ('valid', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_frames', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_frames', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='api.project')),
                ('sequence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='api.sequence')),
                ('shot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='api.shot')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_frames', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': [('add_any_entity', 'Can add entity that belong to a project the user does not own'), ('change_any_entity', 'Can change entity that belong to a project the user does not own'), ('delete_any_entity', 'Can delete entity that belong to a project the user does not own')],
                'unique_together': {('index', 'project', 'sequence', 'shot'), ('project', 'sequence', 'shot', 'root')},
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('root', models.CharField(max_length=250, null=True, validators=[api.validators.path_validator])),
                ('state', models.CharField(max_length=10, validators=[api.validators.state_validator])),
                ('framerate', models.FloatField(default=25.0)),
                ('width', models.PositiveIntegerField(default=1920)),
                ('height', models.PositiveIntegerField(default=1080)),
                ('name', models.SlugField(default='untitled', unique=True)),
                ('label', models.CharField(default='untitled', max_length=250)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_assets', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_assets', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='api.project')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_assets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': [('add_any_entity', 'Can add entity that belong to a project the user does not own'), ('change_any_entity', 'Can change entity that belong to a project the user does not own'), ('delete_any_entity', 'Can delete entity that belong to a project the user does not own')],
                'unique_together': {('project', 'root'), ('name', 'project')},
            },
        ),
    ]
