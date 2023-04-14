from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class Ping(GenericAPIView):
    def get(self, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
