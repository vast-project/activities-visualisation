# Generated by Django 4.0.2 on 2023-04-09 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity_data', '0019_rename_useid_user_userid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('userid', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('activity', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.activity')),
                ('age', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.age')),
                ('education', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.education')),
                ('gender', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.gender')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='usertype',
            name='language_local',
        ),
        migrations.RenameModel(
            old_name='UserGroup',
            new_name='VisitorGroup',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='UserType',
        ),
        migrations.AddField(
            model_name='visitor',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.visitorgroup'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='motherLanguage',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.language'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='nationality',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='activity_data.nationality'),
        ),
    ]