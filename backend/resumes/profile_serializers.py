from rest_framework import serializers
from .models import (
    StudentProfile,
    Education,
    Experience,
    Project,
    Skill,
    Certification,
    Achievement,
    Language
)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id",
            "degree",
            "institution",
            "start_year",
            "end_year",
            "percentage"
        ]
        read_only_fields = ["id"]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id",
            "job_title",
            "company",
            "start_date",
            "end_date",
            "description"
        ]
        read_only_fields = ["id"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "technologies",
            "project_link"
        ]
        read_only_fields = ["id"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "category"
        ]
        read_only_fields = ["id"]


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = [
            "id",
            "name",
            "issuing_organization",
            "issue_date",
            "credential_url"
        ]
        read_only_fields = ["id"]


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = [
            "id",
            "title",
            "description"
        ]
        read_only_fields = ["id"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = [
            "id",
            "name",
            "proficiency"
        ]
        read_only_fields = ["id"]


class StudentProfileSerializer(serializers.ModelSerializer):
    education = EducationSerializer(
        many=True,
        required=False
    )
    experience = ExperienceSerializer(
        many=True,
        required=False
    )
    projects = ProjectSerializer(
        many=True,
        required=False
    )
    skills = SkillSerializer(
        many=True,
        required=False
    )
    certifications = CertificationSerializer(
        many=True,
        required=False
    )
    achievements = AchievementSerializer(
        many=True,
        required=False
    )
    languages = LanguageSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "location",
            "linkedin",
            "github",
            "portfolio",
            "summary",
            "education",
            "experience",
            "projects",
            "skills",
            "certifications",
            "achievements",
            "languages",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]

    def create(self, validated_data):
        education_data = validated_data.pop("education", [])
        experience_data = validated_data.pop("experience", [])
        projects_data = validated_data.pop("projects", [])
        skills_data = validated_data.pop("skills", [])
        certifications_data = validated_data.pop("certifications", [])
        achievements_data = validated_data.pop("achievements", [])
        languages_data = validated_data.pop("languages", [])

        profile = StudentProfile.objects.create(**validated_data)

        for data in education_data:
            Education.objects.create(profile=profile, **data)

        for data in experience_data:
            Experience.objects.create(profile=profile, **data)

        for data in projects_data:
            Project.objects.create(profile=profile, **data)

        for data in skills_data:
            Skill.objects.create(profile=profile, **data)

        for data in certifications_data:
            Certification.objects.create(profile=profile, **data)

        for data in achievements_data:
            Achievement.objects.create(profile=profile, **data)

        for data in languages_data:
            Language.objects.create(profile=profile, **data)

        return profile

    def update(self, instance, validated_data):
        education_data = validated_data.pop("education", None)
        experience_data = validated_data.pop("experience", None)
        projects_data = validated_data.pop("projects", None)
        skills_data = validated_data.pop("skills", None)
        certifications_data = validated_data.pop("certifications", None)
        achievements_data = validated_data.pop("achievements", None)
        languages_data = validated_data.pop("languages", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if education_data is not None:
            instance.education.all().delete()
            for data in education_data:
                Education.objects.create(profile=instance, **data)

        if experience_data is not None:
            instance.experience.all().delete()
            for data in experience_data:
                Experience.objects.create(profile=instance, **data)

        if projects_data is not None:
            instance.projects.all().delete()
            for data in projects_data:
                Project.objects.create(profile=instance, **data)

        if skills_data is not None:
            instance.skills.all().delete()
            for data in skills_data:
                Skill.objects.create(profile=instance, **data)

        if certifications_data is not None:
            instance.certifications.all().delete()
            for data in certifications_data:
                Certification.objects.create(profile=instance, **data)

        if achievements_data is not None:
            instance.achievements.all().delete()
            for data in achievements_data:
                Achievement.objects.create(profile=instance, **data)

        if languages_data is not None:
            instance.languages.all().delete()
            for data in languages_data:
                Language.objects.create(profile=instance, **data)

        return instance
