from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .decorators import check_ownership
from .models import Project
from .serializers import ProjectSerializer


class ProjectView(APIView):

    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post"]

    def get(self, request):
        """
        List all projects.
        """
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new project.
        """
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailsView(APIView):

    permission_classes = (IsAuthenticated,)
    http_method_names = ["delete", "get", "patch"]

    def get_object(self, pk):
        return get_object_or_404(Project, pk=pk)

    def get(self, request, pk):
        """
        Retrieve a project instance by id.
        """
        snippet = self.get_object(pk)
        serializer = ProjectSerializer(snippet)
        return Response(serializer.data)

    @check_ownership
    def patch(self, request, pk):
        """
        Update a project instance. Only project owner can modify projects.
        """
        snippet = self.get_object(pk)
        serializer = ProjectSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_ownership
    def delete(self, request, pk):
        """
        Delete a project instance. Only project owner can delete projects.
        """
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
