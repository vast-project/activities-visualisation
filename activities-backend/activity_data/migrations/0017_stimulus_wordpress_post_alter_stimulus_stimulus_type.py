# Generated by Django 4.2.3 on 2023-08-13 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0016_stimulus_image_stimulus_image_resource_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stimulus',
            name='wordpress_post',
            field=models.CharField(blank=True, choices=[], max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='stimulus',
            name='stimulus_type',
            field=models.CharField(choices=[('Document', 'Document'), ('Segment', 'Segment'), ('Image', 'Image'), ('Audio', 'Audio'), ('Video', 'Video'), ('Tool', 'Tool'), ('Questionnaire', 'Questionnaire')], max_length=32),
        ),
    ]
