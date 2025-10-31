from rest_framework import serializers
from .models import Candidate
import os

def validate_resume_file(value):
    # Allow only pdf/doc/docx
    valid_extensions = ['.pdf', '.doc', '.docx']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise serializers.ValidationError('Resume must be a PDF or Word document (.pdf, .doc, .docx).')
    # Size limit: 5MB
    limit_mb = 5
    if value.size > limit_mb * 1024 * 1024:
        raise serializers.ValidationError(f'Resume file size must be <= {limit_mb} MB')

class CandidateSerializer(serializers.ModelSerializer):
    resume = serializers.FileField(write_only=True, validators=[validate_resume_file])

    class Meta:
        model = Candidate
        fields = (
            'id', 'name', 'address', 'skills', 'github_link', 'age', 
            'resume', 'college_name', 'passing_year', 'email', 'phone_number', 'submitted_at'
        )
        read_only_fields = ('id', 'submitted_at')

    def validate_age(self, value):
        if value < 16:
            raise serializers.ValidationError('Age must be at least 16')
        return value

    def validate_passing_year(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError('Passing year must be a number.')
        return value

    def create(self, validated_data):
        resume_file = validated_data.pop('resume')
        candidate = Candidate.objects.create(resume=resume_file, **validated_data)
        return candidate
