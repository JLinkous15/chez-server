from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
import openai
import os
from dotenv import load_dotenv


class ChatView(ViewSet):
    @action(methods=['post'], detail=False)
    def chatGPT(self, request):
        load_dotenv()
        api_key = os.getenv("OPENAI_KEY", None)

        openai.api_key = api_key

        user_input = request.data['user_input']

        prompt = user_input

        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=500,
            stop=None,
            temperature=0.75
        )
        chatGPT_response = response['choices'][0]['text']
        return Response(f'{chatGPT_response}', status=status.HTTP_201_CREATED)
