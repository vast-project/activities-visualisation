# Generated by Django 4.0.2 on 2023-04-09 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0027_event_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.organisation'),
        ),
    ]
