from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class TravelProject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'travel_projects'
        verbose_name = 'Travel Project'
        verbose_name_plural = 'Travel Projects'

    def __str__(self):
        return self.name

    def can_be_deleted(self):
        return not self.places.filter(is_visited=True).exists()

    @property
    def is_completed(self):
        places = self.places.all()
        if not places.exists():
            return False
        return all(place.is_visited for place in places)

    def clean(self):
        super.clean()
        if self.pk and self.places.count() >= 10:
            raise ValidationError("The project can't have more than 10 places.")


class ProjectPlace(models.Model):
    project = models.ForeignKey(
        TravelProject,
        on_delete=models.CASCADE,
        related_name='places'
    )
    external_id = models.IntegerField(help_text="ID from Art Institute of Chicago API")

    title = models.CharField(max_length=500)
    artist_display = models.CharField(max_length=500, blank=True, null=True)
    date_display = models.CharField(max_length=255, blank=True, null=True)
    place_of_origin = models.CharField(max_length=255, blank=True, null=True)
    artwork_type = models.CharField(max_length=255, blank=True, null=True)
    image_id = models.CharField(max_length=255, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    is_visited = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'project_places'
        verbose_name = 'Project Place'
        verbose_name_plural = 'Project Places'

    def __str__(self):
        return f"{self.title} - {self.project.name}"