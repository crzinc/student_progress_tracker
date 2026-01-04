# In students/urls.py
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path("", views.student_list, name="student_list"),
    path("add/", views.student_create, name="student_add"),
    path("<int:student_id>/", views.student_detail, name="student_detail"),
    path("<int:student_id>/edit/", views.student_edit, name="student_edit"),
    path("<int:student_id>/delete/", views.student_delete, name="student_delete"),
]