from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from chezapi.models import Chef
from rest_framework.decorators import action
from django.contrib.auth.models import User
import uuid
import base64
from django.core.files.base import ContentFile


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

    def destroy(self, request, pk):
        chef = Chef.objects.get(user=request.auth.user)
        chef.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET', 'PUT'], detail=False)
    def getMe(self, request):
        if request.method == "GET":
            user = Chef.objects.get(user=request.auth.user)
            serialized = ChefSerializer(user, many=False)
            return Response(serialized.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            chef = Chef.objects.get(user=request.auth.user)
            user = User.objects.get(pk=chef.user.id)
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            chef.bio = request.data['bio']

            if request.data['image'] != "":
                format, imgstr = request.data["image"].split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(
                    imgstr), name=f'{chef.id}-{uuid.uuid4()}.{ext}')
                chef.profile_image = data
            chef.save()
            user.save()

            return Response(None, status=status.HTTP_200_OK)


class ChefSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ('id', 'username', 'profile_image')


class ChefSerializer(serializers.ModelSerializer):
    subscriptions = ChefSubscriptionSerializer(many=True)

    class Meta:
        model = Chef
        fields = ('id', 'full_name', 'profile_image', 'bio',
                  'username', 'is_chef', 'is_staff', 'subscriptions')
