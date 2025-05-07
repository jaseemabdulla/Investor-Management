from rest_framework import serializers
from accounts.models import BaseUser
from investors.models import InvestorProfile
from mentors.models import MentorProfile
from entrepreneurs.models import EntrepreneurProfile
from admins.models import AdminProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = BaseUser
        fields = ['email', 'username', 'phone_number', 'password', 'role']
        
    def create(self, validated_data):
        role = validated_data.get('role')
        user = BaseUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username'),
            phone_number=validated_data['phone_number'],
            role=role,
            password=validated_data['password']
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

        return user       