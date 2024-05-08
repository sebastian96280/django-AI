from .models import tTipe_document
from rest_framework import viewsets, permissions
from .serializers import projectSerealizer

class ProjectViewSet(viewsets.ModelViewSet):
    #consulta
    queryset = tTipe_document.objects.all()
    #permisos
    permission_classes = [permissions.AllowAny]
    serializer_class = projectSerealizer

