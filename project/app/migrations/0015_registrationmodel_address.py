# Generated by Django 5.0.6 on 2024-06-05 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_registrationmodel_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationmodel',
            name='Address',
            field=models.TextField(null=True),
        ),
    ]
