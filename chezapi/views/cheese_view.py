from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from chezapi.models import Cheese


class CheeseView(ViewSet):
    """Handles requests to /cheeses"""

    def list(self, request):
        """GET requests to /cheeses
        Returns a list of Cheese instances"""
        cheeses = Cheese.objects.all()
        serialized = CheeseSerializer(cheeses, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """GET requests to /cheeses/pk
        Returns an instance of retrieve"""
        cheese = Cheese.objects.get(pk=pk)
        serialized = CheeseSerializer(cheese, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """POST requests to /cheeses
        Returns the created instance of Cheese"""
        cheese = Cheese.objects.create(
            name=request.data['name']
        )
        serialized = CheeseSerializer(cheese, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """PUT requests to /cheeses/pk
        Returns nothing with a 204 status code"""
        cheese = Cheese.objects.get(pk=pk)
        cheese.name = request.data['name']
        cheese.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """DELETE requests to /cheeses/pk
        Returns nothing and a 204 status code"""
        cheese = Cheese.objects.get(pk=pk)
        cheese.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CheeseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheese
        fields = ('id', 'name')
