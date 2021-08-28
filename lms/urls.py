from django.urls import path,include
from django.conf.urls import url
from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin


from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
]