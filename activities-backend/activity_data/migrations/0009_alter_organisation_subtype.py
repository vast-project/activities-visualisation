# Generated by Django 4.0.2 on 2023-03-30 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0008_alter_activity_description_local_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='subtype',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='subtype', to='activity_data.organisationtype'),
        ),
    ]
