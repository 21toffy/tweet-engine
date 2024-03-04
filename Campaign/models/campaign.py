from Common.models import BaseModel
from django.db import models
from Auth.models import User, Profile

import random


class Campaign(BaseModel):
    TYPE_CHOICES = [
        ('match_tweet', 'Match Tweet'),
        ('like_tweet', 'Like Tweet'),
        ('retweet', 'Retweet'),
        ('random_tweet_but_hashtag', 'Random Tweet with Hashtag'),
    ]
    REWARD_CHOICES = [
        ('airtime', 'airtime'),
        ('data', 'data'),
        ('cash', 'cash'),
    ]
    TIME_FREQUENCY_CHOICES = [
        ('hour', 'Hour'),
        ('day', 'Day'),
    ]
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    campaign_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    campaign_hashtags = models.CharField(max_length=50, null=True, blank=True)
    campaign_code = models.CharField(max_length=20)
    point = models.IntegerField(default=0, null=True, blank=True)
    reward = models.CharField(choices=REWARD_CHOICES)
    reward_value = models.DecimalField(default=0.0, decimal_places=2, max_digits= 8)
    tweet = models.TextField(null=True, blank=True)
    tweet_link = models.URLField(null=True, blank=True)
    tweet_number_frequency = models.IntegerField(default=0)
    tweet_time_frequency = models.CharField(choices=TIME_FREQUENCY_CHOICES)
    total_tweets_needed = models.IntegerField(default=0)
    users_needed = models.IntegerField(default=0)
    tweet_number_per_user = models.IntegerField(default=0)
    public = models.BooleanField(default=False)

    def generate_unique_code(self):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.choice(chars) for _ in range(10))
    
    def calculate_users_needed(self):
        if self.total_tweets_needed and self.users_needed and self.tweet_time_frequency:
            frequency_multiplier = 1  # Default to 1 tweet per user if frequency is not specified

            if self.tweet_time_frequency == 'hour':
                frequency_multiplier = 24  # Assuming tweets per hour
            elif self.tweet_time_frequency == 'day':
                frequency_multiplier = 24 * 7  # Assuming tweets per day

            # Calculate tweets_per_user based on total_tweets_needed, users_needed, and frequency
            self.tweet_number_per_user = (
                (self.total_tweets_needed // (self.users_needed * frequency_multiplier)) or 1
            )

            # Calculate users_needed based on total_tweets_needed, tweets_per_user, and frequency
            self.users_needed = (
                (self.total_tweets_needed // max(1, self.tweet_number_per_user)) or 1
            )

    def generate_save_campaign_code(self):
        if not self.campaign_code:
            unique_code = self.generate_unique_code()
            while Campaign.objects.filter(campaign_code=unique_code).exists():
                unique_code = self.generate_unique_code()
            self.campaign_code = unique_code

    def save(self, *args, **kwargs):
        self.calculate_users_needed()
        self.generate_save_campaign_code()
        super().save(*args, **kwargs)

# campaign_code
class Addon(BaseModel):
    min_followers = models.IntegerField(default=300)
    additional_followers_required = models.IntegerField(default=10000)
    tweets_required = models.IntegerField(default=1000)

class UserCampaign(BaseModel):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    points_earned = models.IntegerField()
    total_point = models.IntegerField()
    timestamp = models.DateTimeField()
    completed = models.BooleanField(default=False)


class CampaignRecord(BaseModel):
    user_campaign = models.ForeignKey(UserCampaign, on_delete=models.CASCADE)
    tweet_url = models.URLField()
    points_earned = models.IntegerField()
    point_before = models.IntegerField()
    point_after = models.IntegerField()
    total_point = models.IntegerField()
    timestamp = models.DateTimeField()
    completed = models.BooleanField(default=False)
    valid = models.BooleanField(default=False)



class Penalty(BaseModel):
    user_campaign = models.ForeignKey(UserCampaign, on_delete=models.CASCADE)
    penalty_points = models.IntegerField()
    reason = models.TextField()
    timestamp = models.DateTimeField()