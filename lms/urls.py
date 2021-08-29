from django.urls import path,include
from django.conf.urls import url
from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin


from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('studentSignup', views.handleStudentSignup, name = "studentSignUp"),
    path('teacherSignup', views.handleTeacherSignup, name = "teacherSignUp"),
    path('addSubject', views.addSubject, name = "addSubject"),
    path('login', views.handleLogin, name = "login"),
    path('logout', views.handleLogout, name = "logout"),
]