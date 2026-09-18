from resumes.serializers import ResumeSerializer
from rest_framework.response import Response
from .models import Resume
from rest_framework.views import APIView
from rest_framework import status
from .service import extract_text_from_pdf
from rest_framework.permissions import IsAuthenticated
from .models import StudentProfile
from .profile_serializers import StudentProfileSerializer

# Create your views here.
class ResumeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        resumes = Resume.objects.filter(user = request.user)
        serializer = ResumeSerializer(resumes,many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.save(user=request.user)
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
    
class StudentProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            return Response(
                {"message": "Profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = StudentProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if StudentProfile.objects.filter(user=request.user).exists():
            return Response(
                {"error": "Profile already exists. Use PUT to update it."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = StudentProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save(user=request.user)
            return Response(
                StudentProfileSerializer(profile).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            return Response(
                {"error": "Profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = StudentProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            profile = serializer.save()
            return Response(
                StudentProfileSerializer(profile).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



