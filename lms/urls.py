from django.urls import path, include
from django.conf.urls import url
from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin


from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('studentSignup', views.handleStudentSignup, name="studentSignUp"),
    path('teacherSignup', views.handleTeacherSignup, name="teacherSignUp"),
    path('addSubject', views.addSubject, name="addSubject"),
    path('joinClass', views.joinClass, name="joinClass"),
    path('assignmentSubmission/<str:path_asi_id>',views.submitAssignment, name="submitAssignment"),
    path('assignment/<str:path_asi_id>',views.showAssignment, name="showAssignment"),
    path('addAssignment/<str:path_sub_id>',views.addAssignment, name="addAssignment"),
    path('subject/<str:path_sub_id>', views.showSubject, name="showSubject"),
    path('login', views.handleLogin, name="login"),
    path('logout', views.handleLogout, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
