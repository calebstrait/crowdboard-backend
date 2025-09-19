import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Ad, Billboard, Vote
from .serializers import AdSerializer

# --- Cloudflare Images config ---
CLOUDFLARE_ACCOUNT_ID = "<your_account_id>"
CLOUDFLARE_API_TOKEN = settings.CLOUDFLARE_API_TOKEN


def get_client_ip(request):
    """Helper to extract client IP address"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


# --- API Views ---

@api_view(["GET"])
def ad_list(request):
    """List ads for a given location"""
    location = request.GET.get("location")
    if location:
        billboard = Billboard.objects.filter(name__icontains=location).first()
        if billboard:
            ads = billboard.ads.all().order_by("-votes")
        else:
            ads = []
    else:
        ads = Ad.objects.all().order_by("-votes")

    serializer = AdSerializer(ads, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def vote(request, ad_id):
    """Vote on an ad (up or down), limited to 1 per IP per ad"""
    try:
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        return Response({"error": "Ad not found"}, status=status.HTTP_404_NOT_FOUND)

    ip = get_client_ip(request)
    if Vote.objects.filter(ad=ad, ip_address=ip).exists():
        return Response({"error": "Already voted"}, status=status.HTTP_403_FORBIDDEN)

    direction = request.data.get("direction")
    if direction == "up":
        ad.votes += 1
    elif direction == "down":
        ad.votes -= 1
    else:
        return Response({"error": "Invalid vote"}, status=status.HTTP_400_BAD_REQUEST)

    ad.save()
    Vote.objects.create(ad=ad, ip_address=ip)

    return Response({"id": ad.id, "votes": ad.votes})


@api_view(["POST"])
def get_upload_url(request):
    """Ask Cloudflare for a direct upload URL"""
    resp = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/images/v2/direct_upload",
        headers={"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"},
    )
    return Response(resp.json(), status=resp.status_code)


@api_view(["POST"])
def create_ad(request):
    """Register a new Ad after Cloudflare upload succeeds"""
    caption = request.data.get("caption", "")
    cloudflare_id = request.data.get("cloudflare_id")
    billboard_id = request.data.get("billboard", 1)  # default billboard

    if not cloudflare_id:
        return Response({"error": "Missing cloudflare_id"}, status=400)

    ad = Ad.objects.create(
        billboard_id=billboard_id,
        caption=caption,
        cloudflare_id=cloudflare_id,
    )
    return Response({
        "id": ad.id,
        "caption": ad.caption,
        "votes": ad.votes,
        "image_url": ad.image_url()
    }, status=status.HTTP_201_CREATED)
