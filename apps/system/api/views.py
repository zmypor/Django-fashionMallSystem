#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from .serializers import fashionMallOrderCommentSerializer


class fashionMallOrderCommentAPIView(APIView):
    """ 留言 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = fashionMallOrderCommentSerializer(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        messages.success(request, '评价成功！')
        return Response({'code':'ok'})