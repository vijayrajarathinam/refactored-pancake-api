"""
Tests for models
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email='user@example.com', password='Tester@123'):
    return get_user_model().objects.create_user(email,password)

class ModelTest(TestCase):
    """ test models """

    def test_create_user_with_email_successful(self):
        """ test create user with an email is successful """
        email = "test@example.com"
        password = 'Test@123'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com']
        ]    

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test@123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com', 'Tester@123'
        )                

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """ Test creating a recipe is successful """
        user = get_user_model().objects.create_user(
            'test@example.com', 'Tester@123'
        )
        recipe = models.Recipe.objects.create(
            user = user,
            title = "Sample Recipe Name",
            time_minutes = 5,
            price = Decimal('5.50'),
            description = "Sample Recipe Description",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """ Test creating a recipe is successful """
        user = create_user('test@example.com', 'Tester@123')
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)    