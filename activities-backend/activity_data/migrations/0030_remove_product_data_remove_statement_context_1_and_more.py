# Generated by Django 4.2.1 on 2023-06-13 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activity_data', '0029_rename_context1_statement_context_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='data',
        ),
        migrations.RemoveField(
            model_name='statement',
            name='context_1',
        ),
        migrations.RemoveField(
            model_name='statement',
            name='context_2',
        ),
        migrations.RemoveField(
            model_name='statement',
            name='relation',
        ),
        migrations.AlterField(
            model_name='organisation',
            name='is_visitor',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=3),
        ),
        migrations.AlterField(
            model_name='stimulus',
            name='stimulus_type',
            field=models.CharField(choices=[('Document', 'Document'), ('Segment', 'Segment'), ('Image', 'Image'), ('Audio', 'Audio'), ('Video', 'Video'), ('Tool', 'Tool')], max_length=16),
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(default=None, max_length=255)),
                ('name_md5', models.CharField(blank=True, default=None, editable=False, max_length=16, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name_local', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('description_local', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('language_local', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.language')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Predicate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(default=None, max_length=255)),
                ('name_md5', models.CharField(blank=True, default=None, editable=False, max_length=16, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name_local', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('description_local', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('language_local', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.language')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(default=None, max_length=255)),
                ('name_md5', models.CharField(blank=True, default=None, editable=False, max_length=16, null=True)),
                ('description', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name_local', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('description_local', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('language_local', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.language')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='statement',
            name='object',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='object', to='activity_data.concept'),
        ),
        migrations.AddField(
            model_name='statement',
            name='predicate',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.predicate'),
        ),
        migrations.AddField(
            model_name='statement',
            name='subject',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='subject', to='activity_data.concept'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.producttype'),
        ),
    ]