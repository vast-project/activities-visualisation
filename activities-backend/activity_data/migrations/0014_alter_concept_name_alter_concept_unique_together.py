# Generated by Django 4.2.3 on 2023-08-12 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0013_concepttype_concept_concept_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concept',
            name='name',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='concept',
            unique_together={('name', 'concept_type')},
        ),
    ]