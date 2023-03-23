import json
from rest_framework import status
from rest_framework.test import APITestCase
from chezapi.models import Chez, Chef, Cheese
from rest_framework.authtoken.models import Token
from datetime import date


class ChezTest(APITestCase):

    fixtures = ['users', 'tokens', 'chefs', 'cheeses']
    """
    Tests do not include images or dates.
    """

    def setUp(self):
        self.chef = Chef.objects.first()
        token = Token.objects.get(user=self.chef.user)
        print(self.chef)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_chez(self):
        """
        Ensures a new chez can be created via post
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = '/chezzes'
        # Define Request Body
        data = {
            "chef": 1,
            "name": "Grilled Cheese",
            "recipe": "grill some cheese.",
            "is_published": False,
            "cheeses": [{
                "id": 1,
                "name": "Cheddar"
            }, {
                "id": 2,
                "name": "American"
            }],
            "image": ""
        }

        response = self.client.post(url, data, format="json")

        cheese1 = self.client.get("/cheeses/1")
        cheese2 = self.client.get("/cheeses/2")

        json_response = json.loads(response.content)
        cheese1_response = json.loads(cheese1.content)
        cheese2_response = json.loads(cheese2.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["name"], "Grilled Cheese")
        self.assertEqual(json_response["recipe"], "grill some cheese.")
        self.assertEqual(json_response["chef"]["id"], 1)
        self.assertEqual(json_response["is_published"], False)
        self.assertIn(cheese1_response, json_response["cheeses"],
                      msg="Cheeze not in Chez.cheeses")
        self.assertIn(cheese2_response, json_response["cheeses"],
                      msg="Cheeze not in Chez.cheeses")

    def test_delete_chez(self):
        """
        Ensures that a chez can be removed from the database
        """
        chef = Chef.objects.first()
        chez = Chez()
        chez.chef = chef
        chez.name = "Grilled Cheese"
        chez.recipe = "grill some cheese."
        chez.image = ""
        chez.save()
        url = f'/chezzes/{chez.id}'

        response = self.client.delete(url, None, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_edit_chez(self):
        """
        Ensures a chez can be updated
        """
        chef = Chef.objects.first()
        chez = Chez()
        chez.chef = chef
        chez.name = "Grilled Cheese"
        chez.recipe = "grill some cheese."
        chez.image = ""
        chez.save()

        data = {
            "name": "grilled schmeeze",
            "recipe": "grill some schmeeze",
            "image": "",
            "is_published": False,
            "cheeses": []
        }

        url = f'/chezzes/{chez.id}'

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
