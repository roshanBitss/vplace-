from rest_framework import serializers
from .models import ResumeAnalysis

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