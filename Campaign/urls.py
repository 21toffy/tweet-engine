# urls.py
from django.urls import path
from Campaign.views import join_campaign, view_flags, view_single_campaign, create_campaign

app_name = "campaign"

urlpatterns = [
    path('join-campaign', join_campaign, name='join_campaign'),
    path('create-campaign', create_campaign, name='create_campaign'),
    path('view-flags', view_flags, name='view_flags'),
path('view-single-campaign/<uuid:pk>/', view_single_campaign, name='view_single_campaign'),
]
