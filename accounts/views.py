from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from accounts.models import BaseUser
import random
from django.core.mail import send_mail
from django.conf import settings


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def verify_email(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    try:
        user = BaseUser.objects.get(email=email)
        if user.otp == otp:
            user.email_verified = True
            user.otp = None
            user.save()
            return Response({'message': 'Email verified successfully'})
        else:
            return Response({'error': 'Invalid OTP'}, status=400)
    except BaseUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)        
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer        
    
@api_view(['POST'])
def request_otp(request):
    email = request.data.get('email')

    try:
        user = BaseUser.objects.get(email=email)

        if not user.email_verified:
            return Response({'error': 'Email not verified'}, status=400)

        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.save()

        send_mail(
            'Your OTP for Login',
            f'Your OTP is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response({'message': 'OTP sent to email'})
    except BaseUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)    
    
@api_view(['POST'])
def login_with_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    try:
        user = BaseUser.objects.get(email=email)

        if not user.email_verified:
            return Response({'error': 'Email not verified'}, status=400)

        if user.otp != otp:
            return Response({'error': 'Invalid OTP'}, status=400)

        user.otp = None  # clear used OTP
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

    except BaseUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)    