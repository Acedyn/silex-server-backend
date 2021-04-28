# Generated by Django 3.2 on 2021-04-28 17:51

from django.db import migrations
from django.db.models import Q
from django.contrib.auth.management import create_permissions
from api.models import project_ownership_permissions


def create_developper_group(apps, schema_editor):
    group = apps.get_model("auth", "group")
    permissions = apps.get_model("auth", "permission")
    # Create the developper group
    developper_group = group.objects.create(name="developper")
    developper_group.save()
    # Give all permissions
    developper_group.permissions.set(permissions.objects.all())
    developper_group.save()


def create_developper_group_reverse(apps, schema_editor):
    group = apps.get_model("auth", "group")
    # Delete the developper group
    group.objects.filter(name="developper").delete()


def create_supervisor_group(apps, schema_editor):
    group = apps.get_model("auth", "group")
    permissions = apps.get_model("auth", "permission")
    # Create the supervisor group
    supervisor_group = group.objects.create(name="supervisor")
    supervisor_group.save()
    # Give permissions to create and edit all projects
    permission_filter = Q()
    for permission in project_ownership_permissions:
        permission_filter = permission_filter | Q(codename=permission[0])
    supervisor_group.permissions.add(
        *list(permissions.objects.filter(permission_filter))
    )
    supervisor_group.save()


def create_supervisor_group_reverse(apps, schema_editor):
    group = apps.get_model("auth", "group")
    # Delete the supervisor group
    group.objects.filter(name="supervisor").delete()


def create_student_group(apps, schema_editor):
    group = apps.get_model("auth", "group")
    # Create the student group
    student_group = group.objects.create(name="student")
    student_group.save()


def create_student_group_reverse(apps, schema_editor):
    group = apps.get_model("auth", "group")
    # Delete the student group
    group.objects.filter(name="student").delete()


def create_initial_groups(apps, schema_editor):
    # Hack to make sure the permissions are created before assigning them to groups
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    create_developper_group(apps, schema_editor)
    create_supervisor_group(apps, schema_editor)
    create_student_group(apps, schema_editor)


def create_initial_groups_reverse(apps, schema_editor):
    create_developper_group_reverse(apps, schema_editor)
    create_supervisor_group_reverse(apps, schema_editor)
    create_student_group_reverse(apps, schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            code=create_initial_groups, reverse_code=create_initial_groups_reverse
        ),
    ]