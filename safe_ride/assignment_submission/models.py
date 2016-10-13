from django.db import models


# Create your models here.

class AssignmentSubmission(models.Model):
    student_id = models.CharField(max_length=200)
    assignment_name = models.CharField(max_length=255)
    output = models.TextField()
    script_hash = models.TextField()
    email_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    total_points = models.IntegerField()

    def __unicode__(self):
        return self.student_id
