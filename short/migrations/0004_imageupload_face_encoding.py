# Generated by Django 5.0.4 on 2024-04-25 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('short', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageupload',
            name='face_encoding',
            field=models.BinaryField(null=True),
        ),
    ]
