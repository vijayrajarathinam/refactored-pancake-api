"""
Test ingredients API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse("recipe:ingredient-list")


def detail_url(tag_id):
    return reverse('recipe:ingredient-detail', args=[tag_id])

def create_user(email='user@example.com', password='Tester@123'):
    return get_user_model().objects.create_user(email,password)


class PublicIngredientApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(INGREDIENT_URL) 
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Ingredient.objects.create(user=self.user, name="Vegan")
        Ingredient.objects.create(user=self.user, name="Dessert")

        res = self.client.get(INGREDIENT_URL) 
        tags = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)