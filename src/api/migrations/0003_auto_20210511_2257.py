# Generated by Django 3.2 on 2021-05-11 22:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_projecttest'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttest',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_projecttest', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projecttest',
            name='deleted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_projecttest', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projecttest',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_projecttest', to=settings.AUTH_USER_MODEL),
        ),
    ]
