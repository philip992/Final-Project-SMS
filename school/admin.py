from django.contrib import admin
from .models import Student, Subject, Enrollment, Grade

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'sex')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('sex',)

admin.site.register(Student, StudentAdmin)
admin.site.register(Subject)
admin.site.register(Enrollment)
admin.site.register(Grade)
