from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

def resume_upload_to(instance, filename):
    return f"resumes/{instance.email}/{filename}"

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    skills = models.CharField(max_length=512, help_text="Comma separated list of skills")
    github_link = models.URLField(blank=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(16), MaxValueValidator(120)])
    resume = models.FileField(upload_to=resume_upload_to)
    
    # Education fields moved here
    college_name = models.CharField(max_length=255)
    passing_year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"
