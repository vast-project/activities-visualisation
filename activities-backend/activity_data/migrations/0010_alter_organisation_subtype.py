# Generated by Django 4.0.2 on 2023-03-30 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0009_alter_organisation_subtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='subtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='subtype', to='activity_data.organisationtype'),
        ),
    ]