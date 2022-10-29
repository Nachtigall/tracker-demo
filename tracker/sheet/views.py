from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .decorators import check_ownership
from .models import Sheet
from .serializers import SheetSerializer


class SheetView(APIView):

    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post"]

    def get(self, request):
        """
        List all sheets of all users of projects user belongs to.
        """
        user_projects = [project.id for project in request.user.projects.all()]
        sheets = Sheet.objects.filter(project_id__in=user_projects)
        serializer = SheetSerializer(sheets, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new sheet for specified project.
        """
        serializer = SheetSerializer(data=request.data)
        if serializer.is_valid():
            if int(request.data["user"]) == request.user.id and int(
                request.data["project"]
            ) in [project.id for project in request.user.projects.all()]:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                "Only own timesheet for involved projects can be created",
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SheetDetailsView(APIView):

    permission_classes = (IsAuthenticated,)
    http_method_names = ["delete", "get", "patch"]

    def get_object(self, pk, request):
        user_projects = [project.id for project in request.user.projects.all()]
        return get_object_or_404(Sheet, pk=pk, project_id__in=user_projects)

    def get(self, request, pk):
        """
        Retrieve a sheet instance by id.
        """
        snippet = self.get_object(pk, request)
        serializer = SheetSerializer(snippet)
        return Response(serializer.data)

    @check_ownership
    def patch(self, request, pk):
        """
        Update a sheet instance. Only sheet owner can modify sheet.
        """
        snippet = self.get_object(pk, request)
        serializer = SheetSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_ownership
    def delete(self, request, pk):
        """
        Delete a sheet instance. Only sheet owner can delete sheet.
        """
        snippet = self.get_object(pk, request)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
