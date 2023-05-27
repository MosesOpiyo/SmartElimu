from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from .serializers import *
from .models import *

@csrf_exempt
@api_view(['POST'])
def admin_registration_view(request):
    
    serializer = RegistrationSerializer(data=request.data)
    admin_serializer = AdminRegistrationSerializer(data=request.data)
    data = {}

    if admin_serializer.is_valid():
        account = admin_serializer.save()  
        data['response'] = f"Successfully created a new user under {account.username} with email {account.email}"
        return Response(data,status = status.HTTP_201_CREATED)
    else:
        data = serializer.errors
        print(serializer.errors)
        return Response(data,status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt 
@api_view(['POST'])
def registration_view(request):
    
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if request.user:
        if serializer.is_valid():
            account = serializer.save(request)  
            data['response'] = f"Successfully created a new user under {account.username} with email {account.email}"
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            print(serializer.errors)
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    else:
        data['response'] = f"No admin for new user"
        return Response(data,status = status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):

    data = {}
    profile = Profile.objects.select_related('user').get(user=request.user)
    data =  ProfileSerializer(profile).data
    return Response(data,status = status.HTTP_200_OK)