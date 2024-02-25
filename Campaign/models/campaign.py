from Common.models import BaseModel
from django.db import models
from Auth.models import User, Profile



class Campaign(BaseModel):
    TYPE_CHOICES = [
        ('match_tweet', 'Match Tweet'),
        ('like_tweet', 'Like Tweet'),
        ('retweet', 'Retweet'),
        ('random_tweet_but_hashtag', 'Random Tweet with Hashtag'),
    ]

    campaign_name = models.CharField(max_length=100)
    campaign_status = models.CharField(max_length=20)
    date = models.DateTimeField()
    campaign_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    campaign_hashtags = models.CharField(max_length=50)
    campaign_code = models.CharField(max_length=20)
    point = models.IntegerField()
    reward = models.CharField(max_length=50)
    tweet = models.TextField(null=True, blank=True)
    tweet_link = models.URLField(null=True, blank=True)
    tweet_number_per_user = models.IntegerField()
    tweet_frequency_per_user = models.CharField(max_length=10)
    total_tweets_needed = models.IntegerField()
    users_needed = models.IntegerField()
    onboarded_by_company = models.IntegerField()
    onboarded_by_us = models.IntegerField()

class Addon(BaseModel):
    min_followers = models.IntegerField(default=300)
    additional_followers_required = models.IntegerField(default=10000)
    tweets_required = models.IntegerField(default=1000)

class UserCampaign(BaseModel):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    tweet_url = models.URLField()
    points_earned = models.IntegerField()
    total_point = models.IntegerField()
    timestamp = models.DateTimeField()

class Penalty(BaseModel):
    user_campaign = models.ForeignKey(UserCampaign, on_delete=models.CASCADE)
    penalty_points = models.IntegerField()
    reason = models.TextField()
    timestamp = models.DateTimeField()