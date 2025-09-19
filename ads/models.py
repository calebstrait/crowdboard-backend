from django.db import models

class Billboard(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    billboard = models.ForeignKey(Billboard, on_delete=models.CASCADE, related_name="ads")
    caption = models.CharField(max_length=255, blank=True)
    cloudflare_id = models.CharField(max_length=100, unique=True)
    votes = models.IntegerField(default=0)

    def image_url(self):
        return f"https://imagedelivery.net/<YOUR_ACCOUNT_HASH>/{self.cloudflare_id}/public"
