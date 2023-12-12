# Generated by Django 4.2.5 on 2023-12-12 21:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activity_data', '0047_rename_europeana_urirf_activity_europeana_uriref'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='europeana_uriref',
        ),
        migrations.CreateModel(
            name='EuropeanaCulturalHeritageArtifact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name_md5', models.CharField(blank=True, default=None, editable=False, max_length=64, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('name_local', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('description_local', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(default=None, max_length=512, unique=True)),
                ('europeana_uriref', models.URLField(blank=True, max_length=8000, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('language_local', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity_data.language')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='europeana_ch_artifact',
            field=models.ManyToManyField(blank=True, default=None, to='activity_data.europeanaculturalheritageartifact', verbose_name='Europeana Artifacts'),
        ),
    ]
