from django.shortcuts import render, redirect, get_object_or_404
from Campaign.models import Campaign, UserCampaign, CampaignRecord
from .forms import CampaignForm, CampaignCodeForm
from Auth.models import Profile
from django.contrib import messages
import traceback
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum


# confirm tweet, 1
# deposit to wallet 2


# join campaign
# check for campaing code return error is not exist
# ckeck if user is valid
# check if it is active return error if not
# ckeck if it is public return error is not
# check if the users are complete return error is not


# edit campaign if campaign is active
# manually add users via tweeter user name and email if they are verified

# if all passed

@login_required
def create_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        try:
            if form.is_valid():
                print(form.cleaned_data['active'])
                campaign = form.save(commit=False)
                profile = Profile.objects.filter(user=request.user).first()
                if profile is None:
                    messages.error(request, "profile does not exist please contact Admin")
                    return redirect('campaign:create_campaign')
                campaign.created_by = profile
                campaign.active = form.cleaned_data['active']
                campaign.save()

                messages.success(request, f'Campaign {campaign.campaign_name} successfully created!')
                return redirect('dashboard')  # Redirect to the dashboard or success page
            else:
                messages.error(request, form.errors)
                return redirect('campaign:create_campaign')
        except Exception as e:
            traceback.print_exc()
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('campaign:create_campaign')
    else:
        form = CampaignForm()
    return render(request, 'create_campaign.html', {'form': form})


@login_required
def join_campaign(request):
    if request.method == 'POST':
        form = CampaignCodeForm(request.POST)
        try:
            if form.is_valid():
                campaign_code = form.cleaned_data['campaign_code']
                campaign = Campaign.objects.filter(campaign_code=campaign_code).first()

                if campaign is None:
                    messages.error(request, 'Campaign does not exist. Please check the campaign code.')
                    return redirect('campaign:join_campaign')
                
                if not campaign.active:
                    messages.error(request, 'Campaign is not active.')
                    return redirect('campaign:join_campaign')
                
                enrolled = UserCampaign.objects.filter(campaign=campaign).count()

                if campaign.users_needed <= enrolled:
                    messages.error(request, 'Campaign Already full.')
                    return redirect('campaign:join_campaign')

                user_profile = Profile.objects.filter(user=request.user).first()

                if user_profile is None:
                    messages.error(request, 'Profile does not exist. Please contact Admin.')
                    return redirect('campaign:join_campaign')

                # Check if the campaign is active

                # Check if the campaign is public
                # if not campaign.public:
                #     messages.error(request, 'Campaign is not public.')
                #     return redirect('campaign:join_campaign')

                # Check if the users are complete (you can modify this condition based on your requirement)
                if UserCampaign.objects.filter(campaign=campaign, user_profile=user_profile).exists():
                    messages.error(request, 'You have already joined this campaign.')
                    return redirect('campaign:join_campaign')


                # If all checks pass, create the UserCampaign instance
                user_campaign = UserCampaign.objects.create(
                    user_profile=user_profile,
                    campaign=campaign,
                    points_earned=0,  # You can set the initial points earned as needed
                    total_point=campaign.point,  # Assuming total_point is the total point for the campaign
                    timestamp=timezone.now(),
                    completed=False
                )

                messages.success(request, f'Successfully joined campaign: {campaign.campaign_name}')
                return redirect('dashboard')  # Redirect to the dashboard or success page
            else:
                messages.error(request, 'Invalid form submission. Please check your data.')
                return redirect('campaign:join_campaign')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('campaign:join_campaign')
    else:
        form = CampaignCodeForm()
    return render(request, 'join_campaign.html', {'form': form})

@login_required
def view_flags(request):
    return render(request, 'auth/login.html')


# not owner ?
# total number of CampaignRecord, number valid CampaignRecord, invalid records/penalty, points gained/total atainabe points 
# table with campaign records 
# campaign name, attainable points, points before, points after, valid


# owner ?
# total number of UserCampaign, number valid/completed UserCampaign, invalid records, points gained/total atainabe points 



@login_required
def view_single_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)

    user_campaigns = UserCampaign.objects.filter(campaign=campaign)
    # if request.user == campaign.created_by.user:
    # else:
    user_campaigns = CampaignRecord.objects.filter(user_campaign__user_profile__user=user_campaigns)

    total_participants = user_campaigns.count()
    total_points_earned = user_campaigns.aggregate(Sum('points_earned'))['points_earned__sum']


    context = {
        'campaign': campaign,

        'total_participants': total_participants,

        'total_points_earned': total_points_earned,

        'user_campaigns': user_campaigns,
    }

    return render(request, 'campaign-details.html', context)