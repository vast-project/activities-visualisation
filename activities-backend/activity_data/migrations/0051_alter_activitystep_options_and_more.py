# Generated by Django 5.0.1 on 2024-02-01 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0050_activitystep_step_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitystep',
            options={'ordering': ['name']},
        ),
        migrations.AlterOrderWithRespectTo(
            name='activitystep',
            order_with_respect_to=None,
        ),
    ]
