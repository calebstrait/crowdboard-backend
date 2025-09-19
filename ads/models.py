from django.db import models
from django.utils import timezone


class Billboard(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    billboard = models.ForeignKey(
        Billboard, on_delete=models.CASCADE, related_name="ads"
    )
    caption = models.CharField(max_length=255, blank=True)
    cloudflare_id = models.CharField(max_length=100, unique=True)
    votes = models.IntegerField(default=0)

    def image_url(self):
        """
        Generate a Cloudflare Images delivery URL.
        Replace <YOUR_ACCOUNT_HASH> with the hash from your Cloudflare Images dashboard.
        """
        return f"https://imagedelivery.net/<YOUR_ACCOUNT_HASH>/{self.cloudflare_id}/public"

    def __str__(self):
        return self.caption or f"Ad {self.id}"


class Vote(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="votes_log")
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("ad", "ip_address")  # One vote per IP per ad

    def __str__
