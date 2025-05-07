from django.contrib.auth.models import AbstractUser
from django.db import models

class BaseUser(AbstractUser):
    ROLES = (
        ('investor', 'Investor'),
        ('entrepreneur', 'Entrepreneur'),
        ('admin', 'Admin'),
        ('mentor', 'Mentor'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=False, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    role = models.CharField(max_length=15, choices=ROLES, default='entrepreneur')
    is_blocked = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, unique=True)
    joined_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    email_verified = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email} - {self.role}"



    

    

    
      
    