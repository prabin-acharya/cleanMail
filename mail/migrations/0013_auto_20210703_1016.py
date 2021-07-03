# Generated by Django 3.2.4 on 2021-07-03 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0012_auto_20210627_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='email',
            name='subject',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='email',
            name='timestamp',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='email',
            name='user',
            field=models.EmailField(max_length=254),
        ),
    ]
