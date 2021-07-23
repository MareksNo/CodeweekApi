from django.db import models

class OccupationCategory(models.Model):
    class Meta:
        verbose_name_plural = "Occupation Categories"

    title = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.title}'

class Occupation(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(OccupationCategory, on_delete=models.CASCADE, related_name="occupations")

    def __str__(self):
        return f'{self.category.title}: {self.title}'
