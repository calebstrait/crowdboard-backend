from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Ad, Billboard
from .serializers import AdSerializer

@api_view(["GET"])
def ad_list(request):
    # Example: /ads/?location=allentown
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
    try:
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        return Response({"error": "Ad not found"}, status=status.HTTP_404_NOT_FOUND)

    direction = request.data.get("direction")
    if direction == "up":
        ad.votes += 1
    elif direction == "down":
        ad.votes -= 1
    else:
        return Response({"error": "Invalid vote"}, status=status.HTTP_400_BAD_REQUEST)

    ad.save()
    return Response({"id": ad.id, "votes": ad.votes})
