from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Student(models.Model):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    absent_count = models.PositiveIntegerField(default=0)   # Tracks absences
    present_count = models.PositiveIntegerField(default=0)  # Tracks present days

    def __str__(self):
        return self.user.get_full_name()

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student} - {self.subject}"

class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.subject.name})"

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)  
    exam_score = models.FloatField(null=True, blank=True)
    quiz_score = models.FloatField(null=True, blank=True)
    activity_score = models.FloatField(null=True, blank=True)
    grade = models.FloatField(null=True, blank=True)
    done = models.BooleanField(default=False) 

    class Meta:
        unique_together = ('enrollment', 'exam')  

    def __str__(self):
        return f"{self.enrollment} - {self.exam} - Grade: {self.grade}"
