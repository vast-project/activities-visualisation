# Generated by Django 4.0.2 on 2023-04-09 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0022_remove_event_activity_activity_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='Event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.event'),
        ),
    ]
