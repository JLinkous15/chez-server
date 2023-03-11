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
        Returns a list of all Chez instances
        """
        chezzes = Chez.objects.all()
        serialized = ChezSerializer(chezzes, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """
        GET requests to /chezzes/<pk>
        Returns a single instance of Chez
        """
        try:
            chez = Chez.objects.get(pk=pk)
            serialized = ChezSerializer(chez, many=False)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Chez.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class ChezCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'chef', 'body', 'date')


class ChezSerializer(serializers.ModelSerializer):
    chez_comments = ChezCommentSerializer(many=True)

    class Meta:
        model = Chez
        fields = ('id', 'name', 'recipe', 'image', 'chez_comments')
