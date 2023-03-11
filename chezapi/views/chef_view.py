from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from chezapi.models import Chef


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


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ('id', 'full_name', 'username', 'is_chef')
