from django import forms
from .models import Student, Grade

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['sex']  
        labels = {
            'sex': 'Sex',
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['exam_score', 'quiz_score', 'activity_score', 'done']  
        labels = {
            'exam_score': 'Exam Score',
            'quiz_score': 'Quiz Score',
            'activity_score': 'Activity Score',
            'done': 'Exam Status',  
        }
        widgets = {
            'done': forms.RadioSelect(choices=[(True, 'Done'), (False, 'Not Done')]),  
        }
