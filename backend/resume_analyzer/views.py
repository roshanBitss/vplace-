from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from resumes.models import Resume
from .models import ResumeAnalysis
from .serializers import ResumeAnalysisSerializer
from .services.analyzer import ResumeAnalyzer 
from jobs.models import Job
from .models import ResumeJDMatch
from .serializers import ResumeJDMatchSerializer
from .services.jd_matcher import ResumeJDMatcher
from .services.scoring import (
    calculate_technical_match,
    calculate_experience_match,
    calculate_overall_match
)

# Create your views here.

class ResumeAnalysisView(APIView):
    def post(self,request,resume_id):
        try:
            resume = Resume.objects.get(id = resume_id)
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found"},
                status = status.HTTP_404_NOT_FOUND
            )
        if not resume.extracted_text:
            return Response(
                {"error": "Resume text not availabe"},
                status = status.HTTP_400_BAD_REQUEST
            )
        try:
            analyzer = ResumeAnalyzer()
            analysis_data = analyzer.analyze(resume.extracted_text)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        analysis = ResumeAnalysis.objects.update_or_create(
            resume = resume,
            defaults={
                "ats_score":analysis_data.get("ats_score"),
                "summary":analysis_data.get("summary"),
                "skills":analysis_data.get("skills"),
                "strengths":analysis_data.get("strengths"),
                "weaknesses":analysis_data.get("weaknesses"),
                "recommendations":analysis_data.get("recommendations")
            }
            
        )[0]

        serializer = ResumeAnalysisSerializer(analysis)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ResumeJDMatchView(APIView):
    def post(self,request):
        resume_id = request.data.get("resume_id")
        job_id = request.data.get("job_id")

        if not resume_id or not job_id:
            return Response(
                {
                    "error": "Resume id and Job id are required",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            resume = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            return Response(
                {
                    "error": "Resume not found",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response(
                {
                    "error": "Job not found",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not resume.extracted_text:
            return Response(
                {
                    "error": "Resume text not available",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            matcher = ResumeJDMatcher()
            result = matcher.match(
                resume_text = resume.extracted_text,
                job_role = job.job_role,
                skills_required = job.skills_required,
                job_description = job.job_description
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )


        technical_score = calculate_technical_match(
            job.skills_required or "",
            result.get("matched_skills",[])
        )

        experience_score = calculate_experience_match(
            result.get("experience_evidence",[])
        )

        overall_score = calculate_overall_match(
            technical_score,
            experience_score
        )

        match = ResumeJDMatch.objects.create(
            resume = resume,
            job = job,

            overall_match = overall_score,
            technical_match = technical_score,
            experience_match = experience_score,
            matched_skills = result.get("matched_skills",[]),
            missing_skills = result.get("missing_skills",[]),
            strengths = result.get("strengths",[]),
            skill_gaps = result.get("skill_gaps",[]),
            recommendations = result.get("recommendations",[])

        )

        serializer = ResumeJDMatchSerializer(match)

        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )


            