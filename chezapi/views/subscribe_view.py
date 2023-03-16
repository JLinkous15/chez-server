from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from chezapi.models import Subscribe, Chef
from rest_framework.decorators import action


class SubscribeView(ViewSet):
    """Handles requests to /cheeses"""

    def list(self, request):
        """GET requests to /cheeses
        Returns a list of Cheese instances"""
        subscriptions = Subscribe.objects.all()
        serialized = SubscribeSerializer(subscriptions, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def mySubscriptions(self, request):
        user = Chef.objects.get(user=request.auth.user)
        subscriptions = Subscribe.objects.all()
        subscriptions = subscriptions.filter(chef=user)
        serialized = SubscribeSerializer(subscriptions, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def subscribe(self, request, pk):
        user = Chef.objects.get(user=request.auth.user)
        chef = Chef.objects.get(pk=pk)
        user.subscriptions.add(chef)
        return Response({'message': 'subscription added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unsubscribe(self, request, pk):
        user = Chef.objects.get(user=request.auth.user)
        chef = Chef.objects.get(pk=pk)
        user.subscriptions.remove(chef)
        return Response({'message': 'subscription deleted'}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def amISubscribed(self, request, pk):
        try:
            user = Chef.objects.get(user=request.auth.user)
            chef = Chef.objects.get(pk=pk)
            subscription = Subscribe.objects.get(chef=user, chefscribed=chef)
            return Response(True, status=status.HTTP_200_OK)
        except Subscribe.DoesNotExist:
            return Response(False, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(ex.args[0], status=status.HTTP_404_NOT_FOUND)


class SubscribeChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ('id', 'username')


class SubscribeSerializer(serializers.ModelSerializer):
    chefscribed = SubscribeChefSerializer(many=False)

    class Meta:
        model = Subscribe
        fields = ('id', 'chef', 'chefscribed', 'date')
