from rest_framework import serializers
from accounts.models import BaseUser
from investors.models import InvestorProfile
from mentors.models import MentorProfile
from entrepreneurs.models import EntrepreneurProfile
from admins.models import AdminProfile
import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = BaseUser
        fields = ['email', 'username', 'phone_number', 'password', 'role']
        
    def create(self, validated_data):
        role = validated_data.get('role')
        otp = str(random.randint(100000, 999999))
        user = BaseUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username'),
            phone_number=validated_data['phone_number'],
            role=role,
            password=validated_data['password'],
            otp=otp,
            email_verified=False
        )

        # Create role-specific profile
        if role == 'investor':
            InvestorProfile.objects.create(user=user)
        elif role == 'mentor':
            MentorProfile.objects.create(user=user)
        elif role == 'entrepreneur':
            EntrepreneurProfile.objects.create(user=user)
        elif role == 'admin':
            AdminProfile.objects.create(user=user)
            
        # Send OTP via email
        send_mail(
            'Verify Your Email',
            f'Your verification OTP is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )      

        return user       
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.email_verified:
            raise serializers.ValidationError("Email is not verified.")

        return data

