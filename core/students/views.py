# In students/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from .models import Student
from .forms import StudentForm
from .prediction_service import predictor

def student_list(request):
    """View to display a list of all students."""
    students = Student.objects.all().order_by('-gpa')
    return render(request, "students/student_list.html", {"students": students})

def student_detail(request, student_id):
    """View to display a single student."""
    student = get_object_or_404(Student, id=student_id)

    student_data = {
        'age': student.age,
        'Medu': student.mother_education,
        'Fedu': student.father_education,
        'traveltime': student.travel_time,
        'studytime': student.study_time,
        'failures': student.past_failures,
        'famrel': student.family_relations,
        'freetime': student.free_time,
        'goout': student.go_out,
        'Dalc': student.workday_alcohol,
        'Walc': student.weekend_alcohol,
        'health': student.health_status,
        'absences': student.absences,
    }

    success_probability = student.success_probability
    if success_probability is None:
        success_probability = predictor.predict_success_probability(student_data)

    try:
        success_percentage = int(round(float(success_probability) * 100))
    except Exception:
        success_percentage = 0

    if success_probability is None:
        bar_color_class = 'bg-gray-400'
    elif success_probability >= 0.7:
        bar_color_class = 'bg-green-500'
    elif success_probability >= 0.4:
        bar_color_class = 'bg-yellow-500'
    else:
        bar_color_class = 'bg-red-500'

    raw_factors = predictor.explain(student_data, top_n=5)
    model_factors = []
    for item in raw_factors:
        feature = str(item.get('feature', ''))
        value = item.get('value', None)

        label = feature
        if '_' in feature:
            prefix, suffix = feature.split('_', 1)
            label = f"{prefix}={suffix}"
        elif value is not None:
            try:
                label = f"{feature}={float(value):.0f}"
            except Exception:
                label = f"{feature}={value}"

        model_factors.append(label)

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student,
            "success_probability": success_probability,
            "success_percentage": success_percentage,
            "bar_color_class": bar_color_class,
            "model_factors": model_factors,
        },
    )

def student_create(request):
    """View to create a new student."""
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('students:student_detail', student_id=student.id)
    else:
        form = StudentForm()
    return render(request, "students/student_form.html", {"form": form, "action": "Add"})

def student_edit(request, student_id):
    """View to edit an existing student."""
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            return redirect('students:student_detail', student_id=student.id)
    else:
        form = StudentForm(instance=student)
    return render(request, "students/student_form.html", {"form": form, "action": "Edit"})

def student_delete(request, student_id):
    """View to delete a student."""
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('students:student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})