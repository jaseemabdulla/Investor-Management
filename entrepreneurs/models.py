from django.db import models
from accounts.models import BaseUser
from mentors.models import MentorProfile

class EntrepreneurProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='entrepreneur_profile')
    startup_name = models.CharField(max_length=255)
    business_stage = models.CharField(max_length=100)  # e.g., idea, prototype, revenue
    pitch_deck = models.URLField(blank=True, null=True)
    profile_picture = models.FileField(upload_to='entrepreneur_profile/', blank=True,null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='entrepreneurs')

    def __str__(self):
        return f"EntrepreneurProfile - {self.user.email}"  
