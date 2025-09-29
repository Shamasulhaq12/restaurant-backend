from rest_framework.viewsets import ModelViewSet
from .models import UserProfile
from rest_framework import filters
from utils.paginations.pagination import LimitOffsetPagination
from django_filters import rest_framework as backend_filters
from .filters import UserProfileFilter
from .permissions import IsSuperAdminOrReadOnly
from .serializers import UserProfileSerializer, UserProfileWriteSerializer


class UserProfileViewSet(ModelViewSet):
    permission_classes = [IsSuperAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        backend_filters.DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_class = UserProfileFilter
    search_fields = ['first_name', 'last_name', 'user__username']
    queryset = UserProfile.objects.all()
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserProfileWriteSerializer
        return UserProfileSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or getattr(user, "is_super_admin", False):
            return self.queryset.filter(user__is_active=True)

        if self.action in ['list', 'retrieve']:
            return self.queryset.filter(user__is_active=True)
        return self.queryset.filter(user__is_active=True, user=self.request.user)
