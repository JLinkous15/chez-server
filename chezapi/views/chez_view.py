from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
import uuid
import base64
from django.core.files.base import ContentFile
from rest_framework.decorators import action

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

        chez = Chez.objects.get(pk=pk)
        chez.name = request.data['name']
        chez.recipe = request.data['recipe']
        chez.image = request.data['image']
        chez.save()
        for cheese in request.data["cheeses"]:
            chez.cheeses.add(Cheese.objects.get(pk=cheese['id']))
        try:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(
                imgstr), name=f'chez-{uuid.uuid4()}.{ext}')
            chez.image = data
            chez.save()
            serialized = ChezSerializer(
                chez, many=False, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                imgstr), name=f'chez-{uuid.uuid4()}.{ext}')
            chez.image = data
            chez.save()
            for cheese in request.data["cheeses"]:
                chez.cheeses.add(Cheese.objects.get(pk=cheese['id']))
            serialized = ChezSerializer(
                chez, many=False, context={'request': request})
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=True)
    def postcomment(self, request, pk):

        chez = Chez.objects.get(pk=pk)
        chef = Chef.objects.get(user=request.auth.user)
        comment = Comment()
        comment.chef = chef
        comment.chez = chez
        comment.body = request.data['body']
        try:
            comment.image = None
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        comment.save()
        return Response({'message': "comment added"}, status=status.HTTP_201_CREATED)

    @action(methods=['DELETE'], detail=True)
    def deletecomment(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response({'message': 'comment deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def subscribedChezzes(self, request):
        user = Chef.objects.get(user=request.auth.user)
        chezzes = Chez.objects.filter(chef__in=user.subscriptions.all())
        serialized = ChezSerializer(
            chezzes, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def myChezzes(self, request):
        chef = Chef.objects.get(user=request.auth.user)
        chezzes = Chez.objects.filter(chef=chef)
        serialized = ChezSerializer(
            chezzes, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class ChezCheeseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheese
        fields = ('id', 'name')


class ChezChefSerializer(serializers.ModelSerializer):
    is_chef = serializers.SerializerMethodField()

    class Meta:
        model = Chef
        fields = ('id', 'username', 'is_staff', 'is_chef', 'subscriptions')

    def get_is_chef(self, chef):
        return chef.user == self.context["request"].auth.user


class ChezCommentSerializer(serializers.ModelSerializer):
    chef = ChezChefSerializer(many=False)

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
