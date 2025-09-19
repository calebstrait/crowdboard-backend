from django.db import models

class Billboard(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    billboard = models.ForeignKey(Billboard, on_delete=models.CASCADE, related_name="ads")
    image_url = models.URLField()
    caption = models.CharField(max_length=255, blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.caption or f"Ad {self.id}"
