from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Student, Subject, Enrollment, Grade, Exam
from .forms import StudentForm, GradeForm

def home(request):
    enrolled_students_count = Student.objects.filter(enrollment__active=True).distinct().count()
    teacher_count = User.objects.filter(groups__name='Teachers').count()
    return render(request, 'Home/home.html', {
        'enrolled_students_count': enrolled_students_count,
        'teacher_count': teacher_count,
    })

def teacher_list(request):
    return render(request, 'teachers/teacher_list.html')

def student_list(request):
    query = request.GET.get("q")
    if query:
        students = Student.objects.select_related('user').filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
    else:
        students = Student.objects.select_related('user').all()
    return render(request, 'students/student_list.html', {'students': students})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    subjects = Subject.objects.all()

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            student.user.first_name = request.POST.get('first_name')
            student.user.last_name = request.POST.get('last_name')
            student.user.email = request.POST.get('email')
            student.user.username = request.POST.get('email')
            student.user.save()
            messages.success(request, 'Student details updated successfully.')
            return redirect('student_detail', pk=pk)
    else:
        form = StudentForm(instance=student, initial={
            'first_name': student.user.first_name,
            'last_name': student.user.last_name,
            'email': student.user.email
        })

    return render(request, 'students/student_detail.html', {
        'student': student,
        'form': form,
        'subjects': subjects,
    })

def enroll_student(request):
    subjects = Subject.objects.all()
    student_sex_choices = Student._meta.get_field('sex').choices

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'User with this email already exists.')
            return render(request, 'students/enroll_student.html', {
                'subjects': subjects,
                'student_sex_choices': student_sex_choices,
                'form_data': request.POST,
            })

        user = User.objects.create(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        student = Student.objects.create(
            user=user,
            student_id=request.POST.get('student_id', ''),
            sex=request.POST.get('sex'),
            phone=request.POST.get('phone', ''),
            address=request.POST.get('address', '')
        )

        subject_ids = request.POST.getlist('subjects')
        for subject_id in subject_ids:
            subject = get_object_or_404(Subject, id=subject_id)
            Enrollment.objects.create(student=student, subject=subject)

        messages.success(request, 'Student enrolled successfully.')
        return redirect('student_list')

    return render(request, 'students/enroll_student.html', {
        'subjects': subjects,
        'student_sex_choices': student_sex_choices,
    })

def unenroll_student(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    enrollment.active = False
    enrollment.save()
    messages.success(request, 'Student unenrolled successfully.')
    return redirect('student_detail', pk=enrollment.student.id)

def update_grade(request, enrollment_id, exam_id=None):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    exam = get_object_or_404(Exam, id=exam_id) if exam_id else None

    grade, _ = Grade.objects.get_or_create(enrollment=enrollment, exam=exam)

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grades updated successfully.')
            return redirect('student_detail', pk=enrollment.student.id)
    else:
        form = GradeForm(instance=grade)

    return render(request, 'students/update_grade.html', {
        'form': form,
        'enrollment': enrollment,
        'exam': exam
    })

def edit_grades(request, enrollment_id):
    return update_grade(request, enrollment_id)

def enroll_existing_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id)

        if Enrollment.objects.filter(student=student, subject=subject, active=True).exists():
            messages.warning(request, f"{student.user.get_full_name()} is already enrolled in {subject.name}.")
        else:
            Enrollment.objects.create(student=student, subject=subject, active=True)
            messages.success(request, f"{subject.name} has been successfully enrolled.")

    return redirect('student_detail', pk=student.pk)

def exams(request):
    subjects = Subject.objects.all()
    selected_subject_id = request.GET.get('subject_id')

    selected_subject = None
    enrolled_students = []

    if selected_subject_id:
        selected_subject = get_object_or_404(Subject, id=selected_subject_id)
        enrollments = Enrollment.objects.filter(subject=selected_subject, active=True).select_related('student__user')

        for enrollment in enrollments:
            enrolled_students.append({
                'enrollment': enrollment,
                'student': enrollment.student,
                'grade': None,
            })

    return render(request, 'students/exams.html', {
        'subjects': subjects,
        'selected_subject': selected_subject,
        'enrolled_students': enrolled_students,
    })

def quizzes(request):
    subjects = Subject.objects.all()
    selected_subject_id = request.GET.get('subject_id')

    selected_subject = None
    enrolled_students = []

    if selected_subject_id:
        selected_subject = get_object_or_404(Subject, id=selected_subject_id)
        enrollments = Enrollment.objects.filter(subject=selected_subject, active=True).select_related('student__user')

        for enrollment in enrollments:
            enrolled_students.append({
                'enrollment': enrollment,
                'student': enrollment.student,
                'grade': None,
            })

    return render(request, 'students/quizzes.html', {
        'subjects': subjects,
        'selected_subject': selected_subject,
        'enrolled_students': enrolled_students,
    })

def activities(request):
    subjects = Subject.objects.all()
    selected_subject_id = request.GET.get('subject_id')

    selected_subject = None
    enrolled_students = []

    if selected_subject_id:
        selected_subject = get_object_or_404(Subject, id=selected_subject_id)
        enrollments = Enrollment.objects.filter(subject=selected_subject, active=True).select_related('student__user')

        for enrollment in enrollments:
            enrolled_students.append({
                'enrollment': enrollment,
                'student': enrollment.student,
                'grade': None,
            })

    return render(request, 'students/activities.html', {
        'subjects': subjects,
        'selected_subject': selected_subject,
        'enrolled_students': enrolled_students,
    })

def subjects(request):
    subjects = Subject.objects.all()
    selected_subject_id = request.GET.get('subject_id')
    enrolled_students = []

    if selected_subject_id:
        subject = get_object_or_404(Subject, id=selected_subject_id)
        enrolled_students = Student.objects.filter(
            enrollment__subject=subject,
            enrollment__active=True
        ).select_related('user').distinct()

    return render(request, 'students/subjects.html', {
        'subjects': subjects,
        'enrolled_students': enrolled_students,
        'selected_subject_id': selected_subject_id,
    })

def add_subject(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        name = request.POST.get('name')

        if Subject.objects.filter(id=subject_id).exists():
            messages.error(request, 'Subject ID already exists.')
            return render(request, 'students/add_subject.html', {
                'form_data': request.POST
            })

        Subject.objects.create(id=subject_id, name=name)
        messages.success(request, 'Subject added successfully.')
        return redirect('subjects')

    return render(request, 'students/add_subject.html')

def attendance(request):
    students = Student.objects.select_related('user').all()
    return render(request, 'students/attendance.html', {'students': students})

@csrf_exempt
def mark_attendance(request, student_id, status):
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=student_id)

        if status == 'absent':
            student.absent_count += 1
        elif status == 'present':
            student.present_count += 1
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status.'})

        student.save()
        return JsonResponse({
            'success': True,
            'absent_count': student.absent_count,
            'present_count': student.present_count
        })

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
