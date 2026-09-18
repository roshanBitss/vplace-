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


class ResumeJDMatch(models.Model):
    resume = models.ForeignKey(
        "resumes.Resume",
        on_delete=models.CASCADE,
        related_name="jd_matches"
    )

    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.CASCADE,
        related_name="resume_matches"
    )

    overall_match = models.IntegerField()
    technical_match = models.IntegerField()
    experience_match = models.IntegerField()

    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    strengths = models.JSONField(default=list)
    skill_gaps = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match: {self.resume.title} - {self.job.job_role or self.job.company_name}"
