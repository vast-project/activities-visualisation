# Generated by Django 4.2.3 on 2023-08-25 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0027_alter_questionnaireentry_options_visitor_city_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='questionnaireentry',
            unique_together={('product', 'wpforms_form_id', 'wpforms_entry_id')},
        ),
    ]
