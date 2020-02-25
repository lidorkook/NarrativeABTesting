from django.contrib import admin
from .models import TestSet, TestSetCampaign, TestSetVersion

# Register your models here.
admin.site.register(TestSet)
admin.site.register(TestSetCampaign)
admin.site.register(TestSetVersion)