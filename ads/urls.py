from django.urls import path
from . import views

urlpatterns = [
    path("ads/", views.ad_list, name="ad-list"),
    path("ads/<int:ad_id>/vote/", views.vote, name="ad-vote"),
]
