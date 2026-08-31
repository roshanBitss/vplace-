from resumes.serializers import ResumeSerializer
from rest_framework.response import Response
from .models import Resume
from rest_framework.views import APIView
from rest_framework import status
from .service import extract_text_from_pdf

# Create your views here.
class ResumeAPIView(APIView):
    def get(self,request):
        resumes = Resume.objects.all()
        serializer = ResumeSerializer(resumes,many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.save(user_id=1)
            try:
                extracted_text = extract_text_from_pdf(resume.file)
                # pyrefly: ignore [bad-assignment]
                resume.extracted_text = extracted_text
                resume.save()

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


            return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

