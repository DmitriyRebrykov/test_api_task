from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import TravelProject, ProjectPlace
from .serializers import (
    TravelProjectListSerializer,
    TravelProjectDetailSerializer,
    TravelProjectCreateSerializer,
    TravelProjectUpdateSerializer,
    ProjectPlaceSerializer,
    ProjectPlaceUpdateSerializer,
    AddPlaceToProjectSerializer,
)


class TravelProjectViewSet(viewsets.ModelViewSet):

    queryset = TravelProject.objects.prefetch_related('places').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TravelProjectListSerializer
        elif self.action == 'create':
            return TravelProjectCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TravelProjectUpdateSerializer
        return TravelProjectDetailSerializer

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        if not project.can_be_deleted():
            return Response(
                {
                    'error': 'Cannot delete project with visited places',
                    'detail': 'A project cannot be deleted if any of its places are marked as visited'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='places')
    def list_places(self, request, pk=None):
        project = self.get_object()
        places = project.places.all()
        serializer = ProjectPlaceSerializer(places, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='places/add')
    def add_place(self, request, pk=None):
        project = self.get_object()
        serializer = AddPlaceToProjectSerializer(
            data=request.data,
            context={'project': project}
        )

        if serializer.is_valid():
            place = serializer.save(project=project)
            return Response(
                ProjectPlaceSerializer(place).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='places/(?P<place_id>[^/.]+)')
    def get_place(self, request, pk=None, place_id=None):
        project = self.get_object()
        place = get_object_or_404(ProjectPlace, project=project, id=place_id)
        serializer = ProjectPlaceSerializer(place)
        return Response(serializer.data)

    @action(detail=True, methods=['patch', 'put'], url_path='places/(?P<place_id>[^/.]+)/update')
    def update_place(self, request, pk=None, place_id=None):
        project = self.get_object()
        place = get_object_or_404(ProjectPlace, project=project, id=place_id)

        serializer = ProjectPlaceUpdateSerializer(
            place,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(ProjectPlaceSerializer(place).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)