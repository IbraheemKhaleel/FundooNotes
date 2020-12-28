from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from myfundooNotes.views import Registration
from rest_framework import status
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db

class Data(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.valid_registration_data = {'first_name': "Ibraheem",
                                        'last_name': "Khaleel",
                                        'email': "ibrah@gmail.com",
                                        'user_name': "ibrahkhaleel",
                                        'password': "itisnotmypassport"}
        self.invalid_registration_data = {'first_name': "12",
                                          'last_name': "56",
                                          'email': "abc1",
                                          'user_name': "abc"}
        self.valid_login_data = {
            'email': "ibrah@gmail.com",
            'password': "itisnotmypassport"}
        self.invalid_login_data = {
            'email': "ibrah@gmail.com",
            'password': "itis"}


class RegistrationTests(Data):

    def test_given_valid_details(self):
        """
        Ensure we can create a new account object.
        """

        response = self.client.post(self.register_url, self.valid_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_given_invalid_details(self):
        """
        Ensure we cannot create a new account object.
        """

        response = self.client.post(self.register_url, self.invalid_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(Data):

    def test_given_valid_credentials_login(self):
        """
        Ensure we can login.
        """

        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_active = True
        user.save()

        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_given_invalid_credentials_for_login(self):
        """
        Ensure we cannot login.
        """

        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_active = True
        user.save()

        response = self.client.post(self.login_url, self.invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)