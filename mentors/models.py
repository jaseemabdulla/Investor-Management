from django.db import models
from accounts.models import BaseUser

class MentorProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='mentor_profile')
    expertise_area = models.CharField(max_length=255)
    years_of_experience = models.IntegerField()
    availability = models.BooleanField(default=True)
    profile_picture = models.FileField(upload_to='mentor_profile/', blank=True,null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return f"MentorProfile - {self.user.email}"  
