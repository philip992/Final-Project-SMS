from django.contrib import admin
from .models import Student, Course, Subject, Enrollment, Grade

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id', 'full_name', 'course', 'year_level',
        'status', 'sex', 'nationality', 'phone', 'address'
    )
    list_filter = ('course', 'year_level', 'status', 'sex')
    search_fields = ('student_id', 'first_name', 'last_name')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'active')
    list_filter = ('active', 'subject')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'exam_score', 'quiz_score', 'activity_score')
    list_filter = ('enrollment__subject',)
