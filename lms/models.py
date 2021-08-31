from django.db import models

# Create your models here.


class Student(models.Model):
    student_id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    Class = models.CharField(max_length=3)
    dob = models.DateField()


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)


class Subjects(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_id = models.CharField(
        max_length=10, primary_key=True)  # shown in the slug
    enroll_id = models.CharField(max_length=10, unique=True)
    picture = models.ImageField(upload_to='lms/image', default="")


class Student_Subject(models.Model):
    student_id = models.CharField(max_length=15)
    subject_id = models.CharField(max_length=10)


class Teacher_Subject(models.Model):
    teacher_id = models.CharField(max_length=15)
    subject_id = models.CharField(max_length=10)


class Assignment(models.Model):
    TYPE_CHOICE = [('Asi', 'Assignment'), ('Ass', 'Assesment')]
    assignment_id = models.CharField(max_length=6, primary_key=True)
    assignment_title = models.CharField(max_length=35)
    assignment_pdf = models.FileField(null=True)
    assignment_type = models.CharField(max_length=3, choices=TYPE_CHOICE)
    teacher_id = models.CharField(max_length=15)
    subject_id = models.CharField(max_length=10)
    submission_date = models.DateTimeField(auto_now=True)


class Assignment_Student(models.Model):
    student_id = models.CharField(max_length=15)
    assignment_id = models.CharField(max_length=6)
    status = models.CharField(max_length=25)
    marks = models.IntegerField()
    assignment_pdf = models.FileField(null=True)
    submitted_at = models.DateTimeField(null=True)
