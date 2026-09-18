from django.db import models

# Create your models here.
class Job(models.Model):
        company_name = models.CharField(max_length=255)
        company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
        job_role = models.CharField(max_length=255,null=True, blank=True)
        skills_required = models.TextField(null=True, blank=True)
        job_description = models.TextField(null=True, blank=True)
        last_date_for_submission = models.DateField(null=True, blank=True)
        application_link = models.URLField(null=True, blank=True)

        def __str__(self):
            return f"{self.job_role} at {self.company_name}"