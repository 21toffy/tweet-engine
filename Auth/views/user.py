from django.http import HttpRequest
from django.views.defaults import page_not_found
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from Auth.forms import UserForm, CustomAuthenticationForm
from Auth.models import Profile
from django.db import transaction
from django.contrib.auth import logout

from Campaign.models import Campaign, UserCampaign, Penalty

logger = logging.getLogger("django")

from django.contrib.auth import get_user_model

@login_required
def logout_view(request):
    logout(request)
    return redirect('auth:login')



@transaction.atomic
def register(request):
    if request.method == 'POST':
        try:
            form = UserForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data['email'])
                confirm_password = form.cleaned_data['confirm_password']
                password = form.cleaned_data['password']
                if confirm_password != password:
                    messages.error(request, 'Invalid form submission. Please check your data.')
                    return redirect('auth:register')
                email = form.cleaned_data['email']
                handle = form.cleaned_data['handle']
                User = get_user_model()
                user_exists = User.objects.filter(
                    email=email
                ).first()
                profile_exists = Profile.objects.filter(
                    handle=handle,
                ).first()
                print(email, "JJJJJJJJJJ", user_exists, profile_exists)
                if profile_exists:
                    messages.error(request, 'Twitter handle Exist.')
                    return redirect('auth:register')
                if user_exists:
                    messages.error(request, 'User email Exist.')
                    return redirect('auth:register')    
                user = User.objects.create_user(
                    email=email,
                    password=password,
                )


                profile = Profile.objects.create(
                    user=user,
                    handle=handle,
                )


                print(3333333333, profile.id, profile.user, profile)
                messages.success(request, 'Registration successful. Welcome!')
                print("KKKK")
                return redirect('auth:login')  # Redirect to your home page
            else:
                messages.error(request, 'Invalid form submission. Please check your data.')
                return redirect('auth:register')
        except Exception as e:
            print(str(e), "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKLLLLLLLLLLLLL")
            messages.error(request, 'Invalid form submission. Please check your data.')
            return redirect('auth:register')
    else:
        print("LLLLLLKKKKKJJJJJJJHHHHHHGGGGg")
        form = UserForm()
    return render(request, 'auth/register.html', {'form': form})








def view_profile(request):

    return render(request, 'auth/login.html')


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            messages.error(request, 'Invalid email or password.')
            return redirect('auth:login')
        messages.error(request, 'Invalid form submission. Please check your data.')
        return redirect('auth:login')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


@login_required
def dashboard(request):
    created_campaign = Campaign.objects.filter(
        created_by__user = request.user
    ).count()

    participated_campaign = UserCampaign.objects.filter(
        user_profile__user = request.user
    )

    participated_campaign_count =participated_campaign.count()

    penalty_count = Penalty.objects.filter(
        user_campaign__user_profile__user = request.user, active = True
    ).count()

    completed_penalty_count = participated_campaign.filter(completed=True).count()

    trending_campaigns = Campaign.objects.filter(
        public = True, active=True
    )

    context = {
        "created_campaign": created_campaign,
        "participated_campaign": participated_campaign,
        "participated_campaign_count": participated_campaign_count,
        "penalty_count": penalty_count,
        "trending_campaigns": trending_campaigns,
        'completed_penalty_count': completed_penalty_count

    }
    return render(request, 'dashboard.html', context)



def custom_404_handler(request: HttpRequest, exception):
    # Get request information

    # Log the path, the user making the request, and META information
    logger.warning(
        f"404 Not Found - Path: {request.path} - User: {request.user}",
    )

    # Log the HTTP method
    logger.warning(f"404 Not Found - Method: {request.method}")

    # Log the path and the request body
    logger.warning(
        f"404 Not Found - Path: {request.path} & Body: {request.body}"
    )

    # Log the request information
    logger.warning(f"404 Not Found - Request Information: {request.body} {request.path} {request.user}")

    # Call the default 404 handler to render the error page
    return page_not_found(request, exception)


