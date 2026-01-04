# In students/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student

@receiver(post_save, sender=Student)
def update_student_prediction(sender, instance, **kwargs):
    """Update prediction when student data changes"""
    update_fields = kwargs.get('update_fields')

    relevant_fields = {
        'age', 'mother_education', 'father_education', 'travel_time',
        'study_time', 'past_failures', 'family_relations', 'free_time',
        'go_out', 'workday_alcohol', 'weekend_alcohol', 'health_status', 'absences'
    }

    if update_fields is not None:
        update_fields = set(update_fields)
        if update_fields <= {'success_probability'}:
            return
        if not (update_fields & relevant_fields):
            return

    instance.update_success_probability()