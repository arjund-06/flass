from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length=100)
    Class = models.CharField(max_length = 3)
    dob = models.DateField()

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    

class Subjects(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_id =models.CharField(max_length=10, primary_key=True) #shown in the slug
    enroll_id =models.CharField(max_length=10,unique = True)


class Student_Subject(models.Model):
    student_id = models.CharField(max_length=15)
    subject_id =models.CharField(max_length=10)


class Teacher_Subject(models.Model):
    teacher_id = models.CharField(max_length=15)
    subject_id =models.CharField(max_length=10)