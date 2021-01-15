from django.urls import reverse
from rest_framework import status
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class Data(TestCase):
    """
    this class will initialise all the urls and data and it is inherited by other test classes
    """

    def setUp(self):
        """
        this method setup all the url and data which was required by all test cases
        """
        self.register_url = reverse("register")
        self.login_url = reverse("login")

        self.valid_registration_data = {'first_name': "Ibraheem",
                                        'last_name': "Khaleel",
                                        'email': "IbraheemKhaleel96@gmail.com",
                                        'user_name': "IbraheemKhaleel",
                                        'password': "qwerty12"}

        self.invalid_registration_data = {'first_name': "abc",
                                          'last_name': "def",
                                          'email': "abc123@gmail.com",
                                          'user_name': "abcdef"}
        self.valid_login_data = {
            'email': "IbraheemKhaleel96@gmail.com",
            'password': "qwerty12"}
        self.invalid_login_data = {
            'email': "123abc@gmail.com",
            'password': "abcdef"}


class RegistrationTests(Data):
    """
    this class will test registration view and match with status_code
    """

    def test_given_valid_details_for_registration(self):
        """
        Ensure we can create a new account object and it returns status code as 201.
        """

        response = self.client.post(self.register_url, self.valid_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_given_invalid_details_for_registration(self):
        """
        Ensure we cannot create a new account object and returns status code as 400.
        """

        response = self.client.post(self.register_url, self.invalid_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(Data):

    def test_given_valid_credentials_login(self):
        """
        Ensure we can login and return status code as 200.
        """

        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_given_invalid_credentials_for_login(self):
        """
        Ensure we cannot login and returns status code as 400.
        """

        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_active = True
        user.save()

        response = self.client.post(self.login_url, self.invalid_login_data, format='json')
        assert response.status_code == 400
