from rest_framework import serializers
from django.db import transaction
from .models import TravelProject, ProjectPlace
from .services import ArtInstituteService, ArtInstituteAPIError


class ProjectPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectPlace
        fields = [
            'id', 'external_id', 'title', 'artist_display',
            'date_display', 'place_of_origin', 'artwork_type',
            'image_id', 'notes', 'is_visited', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'title', 'artist_display', 'date_display',
            'place_of_origin', 'artwork_type', 'image_id',
            'created_at', 'updated_at'
        ]


class ProjectPlaceCreateSerializer(serializers.Serializer):
    external_id = serializers.IntegerField(min_value=1)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_external_id(self, value):
        if not ArtInstituteService.validate_artwork_exists(value):
            raise serializers.ValidationError(
                f"Artwork with ID {value} does not exist in Art Institute API"
            )
        return value


class ProjectPlaceUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectPlace
        fields = ['notes', 'is_visited']


class TravelProjectListSerializer(serializers.ModelSerializer):
    places_count = serializers.SerializerMethodField()
    is_completed = serializers.ReadOnlyField()

    class Meta:
        model = TravelProject
        fields = [
            'id', 'name', 'description', 'start_date',
            'places_count', 'is_completed', 'created_at', 'updated_at'
        ]

    def get_places_count(self, obj):
        return obj.places.count()


class TravelProjectDetailSerializer(serializers.ModelSerializer):
    places = ProjectPlaceSerializer(many=True, read_only=True)
    is_completed = serializers.ReadOnlyField()

    class Meta:
        model = TravelProject
        fields = [
            'id', 'name', 'description', 'start_date',
            'places', 'is_completed', 'created_at', 'updated_at'
        ]


class TravelProjectCreateSerializer(serializers.ModelSerializer):
    places = ProjectPlaceCreateSerializer(many=True, required=False)

    class Meta:
        model = TravelProject
        fields = ['name', 'description', 'start_date', 'places']

    def validate_places(self, value):
        if value and len(value) > 10:
            raise serializers.ValidationError(
                "A project cannot have more than 10 places"
            )

        if value and len(value) < 1:
            raise serializers.ValidationError(
                "A project must have at least 1 place"
            )

        external_ids = [place['external_id'] for place in value]
        if len(external_ids) != len(set(external_ids)):
            raise serializers.ValidationError(
                "Cannot add the same place multiple times to a project"
            )

        return value

    @transaction.atomic
    def create(self, validated_data):
        places_data = validated_data.pop('places', [])
        project = TravelProject.objects.create(**validated_data)

        # Create places if provided
        for place_data in places_data:
            external_id = place_data['external_id']
            notes = place_data.get('notes', '')

            try:
                artwork_data = ArtInstituteService.get_artwork(external_id)
                if artwork_data:
                    place_info = ArtInstituteService.extract_place_data(artwork_data)
                    ProjectPlace.objects.create(
                        project=project,
                        notes=notes,
                        **place_info
                    )
            except ArtInstituteAPIError:
                ProjectPlace.objects.create(
                    project=project,
                    external_id=external_id,
                    title=f"Artwork {external_id}",
                    notes=notes
                )

        return project


class TravelProjectUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelProject
        fields = ['name', 'description', 'start_date']


class AddPlaceToProjectSerializer(serializers.Serializer):
    external_id = serializers.IntegerField(min_value=1)
    notes = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_external_id(self, value):
        if not ArtInstituteService.validate_artwork_exists(value):
            raise serializers.ValidationError(
                f"Artwork with ID {value} does not exist in Art Institute API"
            )
        return value

    def validate(self, data):
        project = self.context.get('project')
        external_id = data['external_id']

        if project.places.count() >= 10:
            raise serializers.ValidationError(
                "A project cannot have more than 10 places"
            )

        if project.places.filter(external_id=external_id).exists():
            raise serializers.ValidationError(
                "This place is already in the project"
            )

        return data

    def save(self, project):
        external_id = self.validated_data['external_id']
        notes = self.validated_data.get('notes', '')

        artwork_data = ArtInstituteService.get_artwork(external_id)
        if artwork_data:
            place_info = ArtInstituteService.extract_place_data(artwork_data)
            return ProjectPlace.objects.create(
                project=project,
                notes=notes,
                **place_info
            )


        return ProjectPlace.objects.create(
            project=project,
            external_id=external_id,
            title=f"Artwork {external_id}",
            notes=notes
        )