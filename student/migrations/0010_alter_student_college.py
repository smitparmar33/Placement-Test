# Generated by Django 3.2.8 on 2021-10-13 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_auto_20211013_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='college',
            field=models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.CASCADE, to='student.college'),
        ),
    ]
