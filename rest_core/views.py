from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pytz
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import Trip
from .permissions import IsDriver, IsOwner
from .serializers import UserSerializer, TripSerializer

TIME_ZONE = getattr(settings, "TIME_ZONE", 'Europe/Kiev')


def error_404(request, exception):
    data = {'detail': 'page not found. Check README.pdf in project folder to obtain valid URL routes list.'}
    return JsonResponse(data=data, status=404)


class TripViewSet(ViewSet):
    """
    This CBV provide accesses to trips records.
    Accesses allowed only for users how have flag driver=True in their
    profile. Also, only superuser can interact with any user records. Other users
    can view only own records.
    This view supported filtering trips by UNIX timestamps range arguments -
    start and end.
    You can use single argument, both together or none to filter your query.
    """

    def list(self, request, user_pk=None):
        date_start = request.query_params.get('start', None)
        date_end = request.query_params.get('end', None)

        # uncomment this and comment get_permissions method to change view
        # behavior with users who are not a drivers from raising standard 403 error
        # to 401 error

        # user = User.objects.get(pk=user_pk)
        # if not user.profile.driver:
        #     return Response({'detail': 'user is not a driver.'}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = Trip.objects.all()
        trips = queryset.filter(user=user_pk)

        filters = {}
        tz = pytz.timezone(TIME_ZONE)

        # try/except preventing malformed timestamps to crash service
        if date_start:
            try:
                py_date_start = datetime.fromtimestamp(int(date_start), tz)
                filters['start__lte'] = py_date_start
            except Exception as err:
                err_msg = {'detail': 'start argument: {}'.format(err.strerror.lower())}
                return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)

        if date_end:
            try:
                py_date_end = datetime.fromtimestamp(int(date_end), tz)
                filters['end__gte'] = py_date_end
            except Exception as err:
                err_msg = {'detail': 'end argument: {}'.format(err.strerror.lower())}
                return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)

        trips = trips.filter(**filters)

        serializer = TripSerializer(trips, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None, user_pk=None):
        queryset = Trip.objects.all().select_related('user')
        try:
            trip = get_object_or_404(queryset, pk=pk, user=user_pk)
        except ValueError as err:
            err_msg = {'detail': 'pk_argument: {}'.format(err.strerror.lower())}
            return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)

        serializer = TripSerializer(trip)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsDriver, IsOwner]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class UserViewSet(ModelViewSet):
    """
    This CBV provide accesses to user records.
    Only superuser can interact with any user records. Other users
    can view only own records.
    Filtering supported only by primary key.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, user_pk=None, **kwargs):
        queryset = self.get_queryset().prefetch_related('trips')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]