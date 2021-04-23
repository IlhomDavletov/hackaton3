from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from my_profile.models import *
from my_profile.serializers import ProfileSerializer, ReviewSerializer, LikeSerializer, FavouriteSerializer


class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search = self.request.query_params.get('search')
    #     queryset = queryset.filter(
    #         Q(last_name__icontains=search) | Q(first_name__icontains=search)
    #     )
    #     return queryset
    @action(methods=['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().filter(
            Q(last_name__icontains=query) | Q(first_name__icontains=query)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def sort(self, request):
        filter = request.query_params.get('filter')
        if filter == 'hobbies':
            queryset = self.get_queryset().Profile.hobbies.filter(
                Q(hobbies__icontains=filter))

        # elif filter == 'Z-A':
        #     queryset = self.get_queryset().order_by('-title')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class LikeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}

class FavouriteViewSet(ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer


#MARS
# class FavoriteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
#     queryset = Favorite.objects.all()
#     serializer_class = FavoriteSerializer
#     permission_classes = [IsAuthenticated, ]
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.queryset.filter(user=request.user)
#         queryset = self.filter_queryset(queryset)
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
#
#
#     def get_serializer_context(self):
#         return {'request': self.request, 'action': self.action}