from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from resumes.models import Resume
from .models import ResumeAnalysis
from .serializers import ResumeAnalysisSerializer
from .services.analyzer import ResumeAnalyzer 

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
        
            