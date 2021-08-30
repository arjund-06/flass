# Generated by Django 3.2.2 on 2021-08-30 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignment_id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('assignment_title', models.CharField(max_length=35)),
                ('assignment_pdf', models.FileField(null=True, upload_to='')),
                ('type', models.CharField(choices=[('Asi', 'Assignment'), ('Ass', 'Assesment')], max_length=3)),
                ('teacher_id', models.CharField(max_length=15)),
                ('subject_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment_Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=15)),
                ('assignment_id', models.CharField(max_length=6)),
                ('status', models.CharField(max_length=25)),
                ('marks', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='subjects',
            name='picture',
            field=models.CharField(default='', max_length=255),
        ),
    ]