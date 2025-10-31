from django.urls import path
from .views import CandidateCreateAPIView


urlpatterns = [
    path('api/candidates/', CandidateCreateAPIView.as_view(), name='candidate-create'),
]