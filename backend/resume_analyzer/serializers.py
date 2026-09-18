from rest_framework import serializers
from .models import ResumeAnalysis,ResumeJDMatch

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields =[
            "id",
            "ats_score",
            "summary",
            "skills",
            "strengths",
            "weaknesses",
            "recommendations",
            "created_at"
        ]

        read_only_fields= [
            "id",
            "created_at",
        ]

class ResumeJDMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeJDMatch
        fields = [
            "id",
            "resume",
            "job",
            "overall_match",
            "technical_match",
            "experience_match",
            "matched_skills",
            "missing_skills",
            "strengths",
            "skill_gaps",
            "recommendations",
            "created_at"
        ]

        read_only_fields = [
            "id",
            "overall_match",
            "technical_match",
            "experience_match",
            "matched_skills",
            "missing_skills",
            "strengths",
            "skill_gaps",
            "recommendations",
            "created_at",
        ]