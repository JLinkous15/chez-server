import json
from rest_framework import status
from rest_framework.test import APITestCase
from chezapi.models import Article, Chef
from rest_framework.authtoken.models import Token


class ArticleTest(APITestCase):

    fixtures = ['users', 'tokens', 'chefs', 'cheeses']
    """
    Tests do not include images or dates.
    """

    def setUp(self):
        self.chef = Chef.objects.first()
        token = Token.objects.get(user=self.chef.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_article(self):
        """
        Ensures a new article can be created via post
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = '/articles'
        # Define Request Body
        data = {
            "title": "Grilled Cheese",
            "body": "grill some cheese.",
            "image": ""
        }

        response = self.client.post(url, data, format="json")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["title"], "Grilled Cheese")
        self.assertEqual(json_response["body"], "grill some cheese.")
        self.assertEqual(json_response["chef"]["id"], 1)

    def test_delete_article(self):
        """
        Ensures that an article can be removed from the database
        """
        chef = Chef.objects.first()
        article = Article()
        article.chef = chef
        article.title = "Grilled Cheese"
        article.body = "grill some cheese."
        article.image = ""
        article.save()
        url = f'/articles/{article.id}'

        response = self.client.delete(url, None, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_edit_article(self):
        """
        Ensures a article can be updated
        """
        chef = Chef.objects.first()
        article = Article()
        article.chef = chef
        article.title = "Grilled Cheese"
        article.body = "grill some cheese."
        article.image = ""
        article.save()

        data = {
            "title": "grilled schmeeze",
            "body": "grill some schmeeze",
            "image": ""
        }

        url = f'/articles/{article.id}'

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
