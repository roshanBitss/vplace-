from django.urls import path
from .views import ResumeAPIView , StudentProfileAPIView

urlpatterns = [
    path('', ResumeAPIView.as_view(), name='resume-api'),
    path('profile/', StudentProfileAPIView.as_view(), name='student-profile')
]