# Generated by Django 4.2.3 on 2023-08-24 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0023_remove_stimulus_questionnaire_wp_form_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stimulus',
            name='questionnaire',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='stimulus',
            name='questionnaire_wp_post',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='stimulus',
            name='stimulus_type',
            field=models.CharField(choices=[('Document', 'Document'), ('Segment', 'Segment'), ('Image', 'Image'), ('Audio', 'Audio'), ('Video', 'Video'), ('Tool', 'Tool'), ('Questionnaire', 'Questionnaire'), ('Live Performance', 'Live Performance')], max_length=32),
        ),
    ]
