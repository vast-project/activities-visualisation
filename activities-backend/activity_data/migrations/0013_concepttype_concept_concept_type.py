# Generated by Django 4.2.3 on 2023-08-12 21:01

import activity_data.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activity_data', '0012_alter_stimulus_stimulus_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConceptType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name_md5', models.CharField(blank=True, default=None, editable=False, max_length=64, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name_local', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('description_local', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(default=None, max_length=255, unique=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('language_local', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity_data.language')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='concept',
            name='concept_type',
            field=models.ForeignKey(default=activity_data.models.ConceptType.get_default_pk, on_delete=django.db.models.deletion.CASCADE, to='activity_data.concepttype'),
        ),
    ]
