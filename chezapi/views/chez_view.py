from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from chezapi.models import Chez, Chef, Comment


class ChezView(ViewSet):
    """Handle requests to /chezzes"""

    def list(self, request):
        """
        GET requests to /chezzes
        Returns a list of all Chez instances and a 200 status code
        """
        chezzes = Chez.objects.all()
        serialized = ChezSerializer(chezzes, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """
        GET requests to /chezzes/<pk>
        Returns a single instance of Chez and a 200 status code
        """
        try:
            chez = Chez.objects.get(pk=pk)
            serialized = ChezSerializer(chez, many=False)
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
            serialized = ChezSerializer(chez, many=False)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Chez.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        POST requests to /chezzes
        Returns the created instance of Chez and a 201 status code
        """
        chef = Chef.objects.get(user=request.auth.user)
        chez = Chez.objects.create(
            chef=chef,
            name=request.data['name'],
            recipe=request.data['recipe']
        )
        try:
            chez.image = request.data['image']
            chez.save()
        except Exception:
            pass
        serialized = ChezSerializer(chez, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class ChezCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'chef', 'body', 'date')


class ChezSerializer(serializers.ModelSerializer):
    chez_comments = ChezCommentSerializer(many=True)

    class Meta:
        model = Chez
        fields = ('id', 'name', 'recipe', 'image', 'chez_comments')
