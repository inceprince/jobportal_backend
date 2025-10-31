from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CandidateSerializer

class CandidateCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            candidate = serializer.save()
            return Response(CandidateSerializer(candidate).data, status=201)
        return Response(serializer.errors, status=400)
