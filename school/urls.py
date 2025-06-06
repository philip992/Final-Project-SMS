from django.contrib import admin
from django.urls import path
from school import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', views.home, name='home'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.enroll_student, name='enroll_student'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/enroll/', views.enroll_existing_student, name='enroll_existing_student'),
    path('students/unenroll/<int:enrollment_id>/', views.unenroll_student, name='unenroll_student'),

    # Grades
    path('grades/<int:enrollment_id>/edit/', views.edit_grades, name='edit_grades'),
    path('grades/<int:enrollment_id>/exam/<int:exam_id>/', views.update_grade, name='update_grade'),

    # Teachers
    path('teachers/', views.teacher_list, name='teacher_list'),

    # Academics
    path('exams/', views.exams, name='exams'),
    path('quizzes/', views.quizzes, name='quizzes'),
    path('activities/', views.activities, name='activities'), 

    # Subjects
    path('subjects/', views.subjects, name='subjects'),
    path('subjects/add/', views.add_subject, name='add_subject'),

    # Attendance
    path('attendance/', views.attendance, name='attendance'),
    path('attendance/mark/<int:student_id>/<str:status>/', views.mark_attendance, name='mark_attendance'),
]
