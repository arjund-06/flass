from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subjects)
admin.site.register(Student_Subject)
admin.site.register(Teacher_Subject)
admin.site.register(Assignment)
admin.site.register(Assignment_Student)