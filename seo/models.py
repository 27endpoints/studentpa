from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Main Region / Town"

    def __str__(self):
        return self.name


class Subregion(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="subregions")
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Area / Neighborhood"
        unique_together = ('region', 'name')

    def __str__(self):
        return f"{self.name} ({self.region.name})"
