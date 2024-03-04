from django import forms
from .models import Campaign


class CampaignCodeForm(forms.Form):
    campaign_code = forms.CharField(
        label='Campaign Code',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = [
            'campaign_name',
            'campaign_type',
            'users_needed',
            'point',
            'reward',
            'reward_value','tweet',
            'tweet_number_frequency',
            'tweet_time_frequency',
            'total_tweets_needed',
            'public',
            'active',

        ]

        widgets = {
            'campaign_name': forms.TextInput(attrs={'class': 'form-control',}),
            'campaign_type': forms.Select(attrs={'class': 'form-control',}),
            # 'campaign_hashtags': forms.TextInput(attrs={'class': 'form-control',}),
            'point': forms.NumberInput(attrs={'class': 'form-control',}),
            'reward': forms.Select(attrs={'class': 'form-control',}),
            'reward_value': forms.TextInput(attrs={'class': 'form-control',}),
            'tweet': forms.Textarea(attrs={'class': 'form-control',}),
            'tweet_number_frequency': forms.TextInput(attrs={'class': 'form-control',}),
            'tweet_time_frequency': forms.Select(attrs={'class': 'form-control',}),
            'total_tweets_needed': forms.NumberInput(attrs={'class': 'form-control',}),
            'users_needed': forms.NumberInput(attrs={'class': 'form-control',}),
            # 'public': forms.CheckboxInput(attrs={'class': 'form-control text-left ml-0',}),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control col-md-6'

    # TYPE_CHOICES = [
    #     ('match_tweet', 'Match Tweet'),
    # ]
    # TIME_FREQUENCY_CHOICES = [
    #     ('hour', 'Hour'),
    #     ('day', 'Day'),
    # ]
    # campaign_name = forms.CharField(max_length=100)
    # campaign_type = forms.ChoiceField(choices=TYPE_CHOICES)
    # campaign_hashtags = forms.CharField(max_length=50)
    # point = forms.IntegerField()
    
    # reward = forms.CharField(max_length=50)
    # reward_value = forms.DecimalField(default=0.0)
    # tweet = forms.CharField(widget=forms.Textarea, required=False)

    # tweet_number_per_user = forms.IntegerField()
    # tweet_number_frequency = forms.CharField(max_length=10)
    # tweet_time_frequency = forms.CharField(choices=TIME_FREQUENCY_CHOICES)
    # total_tweets_needed = forms.IntegerField()
    # users_needed = forms.IntegerField()
    # public = forms.BooleanField(default=False)

