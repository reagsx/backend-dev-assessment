from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets

from candidates.models import Candidate
from candidates.serializers import CandidateSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    # Filtering and Ordering support
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('reviewed', )
    ordering_fields = ('status', 'date_applied')
