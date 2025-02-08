from django.db import models

# Create your models here.
class City(models.Model):
    city = models.CharField(max_length=100)
    country_code = models.CharField(max_length=50, blank=True, null=True)
    temperature = models.CharField(max_length=10, blank=True, null=True)
    pressure = models.CharField(max_length=10, blank=True, null=True)
    humidity = models.CharField(max_length=10, blank=True, null=True)
    main = models.CharField(max_length=50, blank=True, null=True)
    icon = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city