from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
import uuid
import base64
from django.core.files.base import ContentFile
from chezapi.models import Chez, Chef, Comment, Cheese


class ChezView(ViewSet):
    """Handle requests to /chezzes"""

    def list(self, request):
        """
        GET requests to /chezzes
        Returns a list of all Chez instances and a 200 status code
        """
        chezzes = Chez.objects.all()
        serialized = ChezSerializer(
            chezzes, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """
        GET requests to /chezzes/<pk>
        Returns a single instance of Chez and a 200 status code
        """
        try:
            chez = Chez.objects.get(pk=pk)
            serialized = ChezSerializer(
                chez, many=False, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Chez.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """
        DELETE requests to /chezzes/pk
        Returns nothing except a 204 status code
        """
        try:
            chez = Chez.objects.get(pk=pk)
            chez.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Chez.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        """
        PUT requests to /chezzes/pk
        Returns the updated instance of Chez and a 200 status code
        """
        try:
            chez = Chez.objects.get(pk=pk)
            chez.name = request.data['name']
            chez.recipe = request.data['recipe']
            chez.image = request.data['image']
            chez.save()
            for cheese in request.data["cheeses"]:
                chez.cheeses.add(Cheese.objects.get(pk=cheese['id']))
            serialized = ChezSerializer(
                chez, many=False, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Chez.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        POST requests to /chezzes
        Returns the created instance of Chez and a 201 status code
        """
        chef = Chef.objects.get(user=request.auth.user)
        chez = Chez()
        chez.chef = chef
        chez.name = request.data['name']
        chez.recipe = request.data['recipe']

        try:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(
                imgstr), name=f'{request.data["image"]}-{uuid.uuid4()}.{ext}')
            chez.image = None
            chez.save()
            for cheese in request.data["cheeses"]:
                chez.cheeses.add(Cheese.objects.get(pk=cheese['id']))
            serialized = ChezSerializer(
                chez, many=False, context={'request': request})
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChezCheeseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheese
        fields = ('id', 'name')


class ChezChefSerializer(serializers.ModelSerializer):
    is_chef = serializers.SerializerMethodField()

    class Meta:
        model = Chef
        fields = ('id', 'username', 'is_staff', 'is_chef')

    def get_is_chef(self, chef):
        return chef.user == self.context["request"].auth.user


class ChezCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'chef', 'body', 'date')


class ChezSerializer(serializers.ModelSerializer):
    chez_comments = ChezCommentSerializer(many=True)
    chef = ChezChefSerializer(many=False)
    cheeses = ChezCheeseSerializer(many=True)

    class Meta:
        model = Chez
        fields = ('id', 'chef', 'name', 'recipe',
                  'image', 'chez_comments', 'cheeses')
