from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Candidate

class CandidateCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('candidate-create')  # Ensure this name matches your urls.py

    def test_create_candidate_success(self):
        resume = SimpleUploadedFile('STR-Order-ORD-20250904-B8F12-receipt (1).pdf', b'%PDF-1.4 test pdf content', content_type='application/pdf')
        payload = {
            'name': 'John Doe',
            'address': '123 Street',
            'skills': 'Django,Python,REST',
            'github_link': 'https://github.com/johndoe',
            'age': 25,
            'resume': resume,
            'college_name': 'ABC College',
            'passing_year': 2020,
            'email': 'john@example.com',
            'phone_number': '+12345678901'
        }
        response = self.client.post(self.url, data=payload, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Candidate.objects.filter(email='john@example.com').exists())
        print(response.data)

    def test_create_candidate_invalid_age(self):
        resume = SimpleUploadedFile('STR-Order-ORD-20250904-B8F12-receipt (1).pdf', b'%PDF-1.4 test', content_type='application/pdf')
        payload = {
            'name': 'Bad Age',
            'skills': 'X',
            'age': 10,
            'college_name': 'X College',
            'passing_year': 2018,
            'email': 'badage@example.com',
            'resume': resume
        }
        response = self.client.post(self.url, data=payload, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn('age', response.data)
        print(response.data)

    def test_create_candidate_bad_resume_extension(self):
        resume = SimpleUploadedFile('resume.exe', b'not a valid file', content_type='application/octet-stream')
        payload = {
            'name': 'Bad Resume',
            'skills': 'X',
            'age': 30,
            'college_name': 'X College',
            'passing_year': 2018,
            'email': 'badresume@example.com',
            'resume': resume
        }
        response = self.client.post(self.url, data=payload, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn('resume', response.data)
        print(response.data)
