from django.urls import reverse
from rest_framework.test import APIClient
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
        self.label_url = reverse("manage-label", kwargs={'pk': 1})
        self.note_post_url = reverse("manage-notes")
        self.note_url = reverse("manage-specific-notes", kwargs={'pk': 1})
        self.note_archived_url = reverse("archived-notes")
        self.single_note_archived_url = reverse("manage-specific-archived", kwargs={'pk': 1})
        self.note_pinned_url = reverse("pinned-notes")
        self.single_note_pinned_url = reverse("manage-specific-pinned-notes", kwargs={'pk': 4})
        self.note_trash_url = reverse("trashed-notes")
        self.single_note_trash_url = reverse("manage-specific-trashed-notes", kwargs={'pk': 1})
        self.note_search_url = reverse("search-notes")+"?search_term="+ "valid"

        self.valid_registration_data = {'first_name': "Ibraheem",
                                        'last_name': "Khaleel",
                                        'email': "IbraheemKhaleel96@gmail.com",
                                        'user_name': "IbraheemKhaleel",
                                        'password': "qwerty12"}

        self.valid_login_data = {
            'email': "IbraheemKhaleel96@gmail.com",
            'password': "qwerty12"}

        self.valid_label_data = {
            'name': "label note",
        }
        self.valid_note_put_data = {
            "title": "randomnote",
            "description": "random description",
            "is_archived": True,
            "is_pinned": True,
            "labels": ["label note"],
            "collaborators": ["IbraheemKhaleel96@gmail.com"]
        }
        self.invalid_note_data = {
            'title': "note title",
            'description': "this is my description",
            'labels': "Qwerty Note",
            'collaborators': ["abc123@gmail.com"]
        }

        self.valid_note_data = {
            "title": "valid note",
            "description": "this is my test note",
            "is_archived": True,
            "is_pinned": True,
            "labels": ["label note"],
            "collaborators": ["IbraheemKhaleel96@gmail.com"]
        }
        self.valid_note_data2 = {
            "title": "valid note 2",
            "description": "this is my 2nd test note",
            "is_trashed": True,
            "labels": ["label note"],
            "collaborators": ["IbraheemKhaleel96@gmail.com"]
        }




class NotesTest(Data):
    """
    Test case for validating Notes class with valid and invalid details.
    """

    def test_notes_with_valid_details(self):
        """
        Test case for validating Labels class with valid details.
        """
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']

        response = self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.put(self.note_url, self.valid_note_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_notes_with_invalid_details(self):
        """
        Test case for validating Labels class with invalid details.
        """
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']

        response = self.client.post(self.note_post_url, self.invalid_note_data, HTTP_AUTHORIZATION=headers,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.put(self.note_url, self.valid_note_put_data, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.note_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ArchivedViewTest(Data):
    """
    Test case for validating ArchivedViewTest class with valid and invalid details.
    """

    def test_archived_view_for_valid_details(self):
        """
        Test case for validating ArchivedView class with valid details.
        """
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=headers, format='json')

        response = client.get(self.note_archived_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(self.single_note_archived_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PinnedViewTest(Data):
    """
    Test case for validating PinnedView class with valid and invalid details.
    """

    def test_pinned_view_for_valid_details(self):
        """
        Test case for validating PinnedView class with valid details.
        """
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=headers, format='json')

        response = client.get(self.note_pinned_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TrashViewTest(Data):

    def test_trash_view_for_valid_details(self):
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data2, HTTP_AUTHORIZATION=headers, format='json')

        response = self.client.get(self.note_trash_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.single_note_trash_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchViewTest(Data):

    def test_search_view_for_valid_details(self):
        client = APIClient()
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        user = User.objects.filter(email=self.valid_registration_data['email']).first()
        user.is_verified = True
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.valid_login_data, format='json')
        headers = response.data['data']
        self.client.post(self.label_url, self.valid_label_data, HTTP_AUTHORIZATION=headers, format='json')
        client.post(self.note_post_url, self.valid_note_data, HTTP_AUTHORIZATION=headers, format='json')
        response = self.client.get(self.note_search_url, HTTP_AUTHORIZATION=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
