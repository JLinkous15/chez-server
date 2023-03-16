from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from chezapi.models import Chef
from rest_framework.decorators import action
from django.contrib.auth.models import User


class ChefView(ViewSet):
    """
    Handles requests to /chefs
    """

    def list(self, request):
        """
        GET requests to /chefs
        Returns a list of all chef instances
        """
        chefs = Chef.objects.all()
        for chef in chefs:
            chef.is_chef = False
            if chef.user == request.auth.user:
                chef.is_chef = True
        serialized = ChefSerializer(chefs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """
        GET requests to /chefs/<pk>
        Returns a single instance of Chef, based on the primary key
        """
        try:
            chef = Chef.objects.get(pk=pk)
            serialized = ChefSerializer(chef, many=False)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Chef.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        """
        PUT request to /chefs/pk for users to update their profile
        """
        chef = Chef.objects.get(user=request.auth.user)
        user = User.objects.get(user=request.auth.user)
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        chef.bio = request.data['bio']
        try:
            chef.profile_image = request.data['profile_image']
        except Exception:
            pass
        chef.save()
        user.save()
        serialized = ChefSerializer(chef, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        chef = Chef.objects.get(user=request.auth.user)
        chef.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def getMe(self, request):
        user = Chef.objects.get(user=request.auth.user)
        serialized = ChefSerializer(user, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ('id', 'full_name', 'username', 'is_chef', 'is_staff')
