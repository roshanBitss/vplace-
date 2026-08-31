from django.db import models

# Create your models here.
class ResumeAnalysis(models.Model):
    resume = models.OneToOneField(
        "resumes.Resume",
        on_delete=models.CASCADE,
        related_name="analysis"
    )

    ats_score = models.IntegerField()
    summary = models.TextField()

    skills = models.JSONField(default=list)
    strengths = models.JSONField(default=list)
    weaknesses = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.resume.title}"
