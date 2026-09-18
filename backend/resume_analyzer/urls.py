from django.urls import path
from .views import ResumeAnalysisView,ResumeJDMatchView

urlpatterns = [
    path("<int:resume_id>/",ResumeAnalysisView.as_view(),name="resume-analysis"),
    path("match/",ResumeJDMatchView.as_view(),name="resume-jd-match")
]