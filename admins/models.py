from django.db import models
from accounts.models import BaseUser

class AdminProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='admin_profile')
    department = models.CharField(max_length=255)
    access_level = models.CharField(max_length=50)
    profile_picture = models.FileField(upload_to='student_profile/', blank=True,null=True)

    def __str__(self):
        return f"AdminProfile - {self.user.email}"  
