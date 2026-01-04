# In students/models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gpa = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New fields for prediction
    mother_education = models.IntegerField(
        "Mother's education", 
        choices=[(0, 'None'), (1, 'Primary (4th grade)'), 
                (2, '5th-9th grade'), (3, 'Secondary'), 
                (4, 'Higher')],
        default=2
    )
    father_education = models.IntegerField(
        "Father's education",
        choices=[(0, 'None'), (1, 'Primary (4th grade)'), 
                (2, '5th-9th grade'), (3, 'Secondary'), 
                (4, 'Higher')],
        default=2
    )
    travel_time = models.IntegerField(
        "Home to school travel time (1-4)",
        choices=[(1, '<15 min'), (2, '15-30 min'), 
                (3, '30-60 min'), (4, '>60 min')],
        default=1
    )
    study_time = models.IntegerField(
        "Weekly study time (1-4)",
        choices=[(1, '<2 hours'), (2, '2-5 hours'), 
                (3, '5-10 hours'), (4, '>10 hours')],
        default=2
    )
    past_failures = models.IntegerField(
        "Number of past class failures (0-4)",
        default=0
    )
    family_relations = models.IntegerField(
        "Quality of family relationships (1-5)",
        choices=[(1, 'Very bad'), (2, 'Bad'), (3, 'Average'),
                (4, 'Good'), (5, 'Excellent')],
        default=4
    )
    free_time = models.IntegerField(
        "Free time after school (1-5)",
        choices=[(1, 'Very low'), (2, 'Low'), (3, 'Average'),
                (4, 'High'), (5, 'Very high')],
        default=3
    )
    go_out = models.IntegerField(
        "Going out with friends (1-5)",
        choices=[(1, 'Very low'), (2, 'Low'), (3, 'Average'),
                (4, 'High'), (5, 'Very high')],
        default=3
    )
    workday_alcohol = models.IntegerField(
        "Workday alcohol consumption (1-5)",
        choices=[(1, 'Very low'), (2, 'Low'), (3, 'Average'),
                (4, 'High'), (5, 'Very high')],
        default=1
    )
    weekend_alcohol = models.IntegerField(
        "Weekend alcohol consumption (1-5)",
        choices=[(1, 'Very low'), (2, 'Low'), (3, 'Average'),
                (4, 'High'), (5, 'Very high')],
        default=1
    )
    health_status = models.IntegerField(
        "Current health status (1-5)",
        choices=[(1, 'Very bad'), (2, 'Bad'), (3, 'Average'),
                (4, 'Good'), (5, 'Very good')],
        default=4
    )
    absences = models.IntegerField(
        "Number of school absences",
        default=0
    )
    success_probability = models.FloatField(
        "Predicted success probability (0-1)",
        null=True,
        blank=True
    )

    def update_success_probability(self):
        from .prediction_service import predictor
        if not self.pk:
            return None
        
        # Prepare student data for prediction
        student_data = {
            'age': self.age,
            'Medu': self.mother_education,
            'Fedu': self.father_education,
            'traveltime': self.travel_time,
            'studytime': self.study_time,
            'failures': self.past_failures,
            'famrel': self.family_relations,
            'freetime': self.free_time,
            'goout': self.go_out,
            'Dalc': self.workday_alcohol,
            'Walc': self.weekend_alcohol,
            'health': self.health_status,
            'absences': self.absences
        }
        self.success_probability = predictor.predict_success_probability(student_data)
        self.__class__.objects.filter(pk=self.pk).update(success_probability=self.success_probability)
        return self.success_probability

    class Meta:
        ordering = ['-created_at']