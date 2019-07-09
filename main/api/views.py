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
            return Response('User with such email not found', status=status.HTTP_404_NOT_FOUND)

        serializer = UserLoginSerializer(user, data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)

        if 'active_organization' not in serializer.validated_data:
            organizations = user.organizations.all()
            print(organizations)
            return Response({
                'active_organization': {
                    'message': 'This field is required',
                    'available_organizations': OrganizationSerializer(organizations, many=True).data
                }
            })

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
        organizations_query = user.organizations.all()
        organizations = OrganizationSerializer(organizations_query, many=True)
        active_organization = OrganizationSerializer(organizations_query[0])
        # First organization in input becomes active
        user.active_organization = organizations_query[0]
        user.save()
        return Response({
            'token': token.key,
            'email': user.email,
            'organizations': organizations.data,
            'active_organization': active_organization.data
        })


class ListOrganizationsView(generics.ListAPIView):
    serializer_class = OrganizationSerializer
    queryset = Organisation.objects.all()


class ListToDosView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):

        print(request.user)
        todo_lists = ToDoList.objects.filter(organization=request.user.active_organization)
        print(todo_lists)
        serializer = ToDoListSerializer(todo_lists, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
