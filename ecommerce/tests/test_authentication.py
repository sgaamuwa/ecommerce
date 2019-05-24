from django.urls import reverse
from rest_framework import status
from ecommerce.tests.test_setup import BaseTestCase
from ecommerce.models import (
    Customer
)


class TestAuthentication(BaseTestCase):
    """
    Class to test the various user authentication endpoints
    Registration and login endpoints
    """

    def test_register_user(self):
        """test a user is created and added to the database"""
        initial_user_count = Customer.objects.count()
        response = self.client.post(
            reverse('register_customer'),
            {
                "username": "samuel",
                "name": "samuel gaamuwa",
                "password1": "pa8ssword123",
                "password2": "pa8ssword123",
                "credit_card": "sam sam",
                "email": "sgaamuwa@gmail.com"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), initial_user_count + 1)

    def test_registration_fails_if_passwords_dont_match(self):
        """test a user is not created if the passwords do not match"""
        initial_user_count = Customer.objects.count()
        response = self.client.post(
            reverse('register_customer'),
            {
                "username": "samuel",
                "name": "samuel gaamuwa",
                "password1": "password123",
                "password2": "pa8ssword123",
                "credit_card": "sam sam",
                "email": "sgaamuwa@gmail.com"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # check that no new users were added
        self.assertEqual(Customer.objects.count(), initial_user_count)

    def test_registration_fails_if_no_credit_card_is_provided(self):
        """test a user is not created if the credit card is not provided"""
        initial_user_count = Customer.objects.count()
        response = self.client.post(
            reverse('register_customer'),
            {
                "username": "samuel",
                "name": "samuel gaamuwa",
                "password1": "password123",
                "password2": "pa8ssword123",
                "email": "sgaamuwa@gmail.com"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # check that no new users were added
        self.assertEqual(Customer.objects.count(), initial_user_count)
