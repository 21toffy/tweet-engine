from django.contrib import admin
from .models import *


admin.site.register(UserCampaign)
admin.site.register(Campaign)
admin.site.register(Penalty)
admin.site.register(CampaignRecord)

