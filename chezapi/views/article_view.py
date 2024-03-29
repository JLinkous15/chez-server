from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
import uuid
import base64
from django.core.files.base import ContentFile
from chezapi.models import Article, Chef


class ArticleView(ViewSet):

    def list(self, request):
        articles = Article.objects.all().order_by("-date")
        serialized = ArticleSerializer(articles, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        POST requests to /chezzes
        Returns the created instance of Chez and a 201 status code
        """
        chef = Chef.objects.get(user=request.auth.user)
        article = Article()
        article.chef = chef
        article.title = request.data['title']
        article.body = request.data['body']

        if request.data['image'] != "":
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(
                imgstr), name=f'article-{uuid.uuid4()}.{ext}')
            article.image = data
            article.save()
        serialized = ArticleSerializer(
            article, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            serialized = ArticleSerializer(article, many=False)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Article.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.title = request.data['title']
        article.body = request.data['body']
        article.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ArticleChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ('id', 'username', 'is_staff')


class ArticleSerializer(serializers.ModelSerializer):
    chef = ArticleChefSerializer(many=False)

    class Meta:
        model = Article
        fields = ('id', 'chef', 'title', 'body', 'date', 'image')
