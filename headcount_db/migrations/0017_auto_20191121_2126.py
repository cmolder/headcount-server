# Generated by Django 2.2.7 on 2019-11-22 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('headcount_db', '0016_auto_20191121_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancetransaction',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='headcount_db.Classroom'),
        ),
        migrations.AlterField(
            model_name='attendancetransaction',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='headcount_db.Student'),
        ),
    ]
