from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from main.models import *
from .serializers import *


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data['email'])
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserLoginSerializer(user, data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            organization = user.organizations.get(pk=request.data['active_organization'])
        except:
            return Response('You do not participate in this organization', status=status.HTTP_400_BAD_REQUEST)

        user.active_organization = organization
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'active_organization': user.active_organization.name
        })


class RegisterView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not Organisation.objects.filter(pk__in=request.data['organizations']).exists():
            return Response('Input correct organizations ids')
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        organizations = OrganizationSerializer(user.organizations.all(), many=True)
        active_organization = OrganizationSerializer(user.organizations.all()[0])
        return Response({
            'token': token.key,
            'email': user.email,
            'organizations': organizations.data,
            'active_organization': active_organization.data
        })


class ListToDos(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):

        list = ToDoList.objects.get(organization=request.user.active_organization)
        todos = ToDo.objects.filter(list=list)

        serializer = ToDoSerializer(todos, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
