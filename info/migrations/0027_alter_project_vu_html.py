# Generated by Django 4.0.1 on 2022-01-07 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0026_project_vu_html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='vu_html',
            field=models.FileField(blank=True, null=True, upload_to='notebooks/'),
        ),
    ]
