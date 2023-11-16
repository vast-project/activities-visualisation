# Generated by Django 4.2.5 on 2023-11-16 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0041_activity_document_activity_document_resource_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='activitystep',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='activitystep',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='activitystep',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='activitystep',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='age',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='age',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='age',
            name='name',
            field=models.CharField(default=None, max_length=512, unique=True),
        ),
        migrations.AlterField(
            model_name='age',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(default=None, max_length=512, unique=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='concept',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='concept',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='concept',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='concept',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='concepttype',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='concepttype',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='concepttype',
            name='name',
            field=models.CharField(default=None, max_length=512, unique=True),
        ),
        migrations.AlterField(
            model_name='concepttype',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='context',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='context',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='context',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='context',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='digitisationapplication',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='digitisationapplication',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='digitisationapplication',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='digitisationapplication',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='education',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='event',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='gender',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='gender',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='gender',
            name='name',
            field=models.CharField(default=None, max_length=512, unique=True),
        ),
        migrations.AlterField(
            model_name='gender',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='nationality',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='nationality',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='nationality',
            name='name',
            field=models.CharField(default=None, max_length=512, unique=True),
        ),
        migrations.AlterField(
            model_name='nationality',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='nature',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='nature',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='nature',
            name='name',
            field=models.CharField(default=None, max_length=512, unique=True),
        ),
        migrations.AlterField(
            model_name='nature',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='organisationtype',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='organisationtype',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='organisationtype',
            name='name',
            field=models.CharField(default=None, max_length=512, unique=True),
        ),
        migrations.AlterField(
            model_name='organisationtype',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='predicate',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='predicate',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='predicate',
            name='name',
            field=models.CharField(default=None, max_length=512, unique=True),
        ),
        migrations.AlterField(
            model_name='predicate',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='productannotation',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='productannotation',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='productannotation',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='productannotation',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='productstatement',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='productstatement',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='productstatement',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='productstatement',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='name',
            field=models.CharField(default=None, max_length=512, unique=True),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaireanswer',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaireanswer',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaireanswer',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='questionnaireanswer',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaireentry',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaireentry',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='questionnaireentry',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='questionnaireentry',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='questionnairequestion',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='questionnairequestion',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='questionnairequestion',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='questionnairequestion',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='statement',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='statement',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='statement',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='statement',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='stimulus',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='stimulus',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='stimulus',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='stimulus',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='visitorgroup',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='visitorgroup',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='visitorgroup',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='visitorgroup',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='visitorgroupqrcode',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='visitorgroupqrcode',
            name='description_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='visitorgroupqrcode',
            name='name',
            field=models.CharField(default=None, max_length=512),
        ),
        migrations.AlterField(
            model_name='visitorgroupqrcode',
            name='name_local',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
    ]
