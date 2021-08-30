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
    path('joinClass', views.joinClass, name = "joinClass"),
    path('subject/<str:path_sub_id>', views.showSubject, name = "showSubject"),
    path('login', views.handleLogin, name = "login"),
    path('logout', views.handleLogout, name = "logout"),
]