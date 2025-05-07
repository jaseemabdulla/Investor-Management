from django.db import models
from accounts.models import BaseUser

class InvestorProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='investor_profile')
    company_name = models.CharField(max_length=255)
    investment_range = models.CharField(max_length=100)
    focus_industries = models.TextField()
    bio = models.TextField(blank=True,null=True)
    profile_picture = models.FileField(upload_to='investor_profile/', blank=True,null=True)

    def __str__(self):
        return f"InvestorProfile - {self.user.email}"
