from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

class Data(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.label_create_url = reverse('label_create_retrieve')
        self.note_create_url = reverse('note_create_retrieve')
        self.note_update_url = reverse('note_update_delete',args=[1])
        

        self.valid_registration_data = {'first_name': "Ibraheem",
                                        'last_name': "Khaleel",
                                        'email': "ikhaleelem@gmail.com",
                                        'user_name': "IbraheemKhaleel",
                                        'password': "random_password"}

        self.valid_label_data ={
            "name": "label1"
        }

        self.valid_note_data = {"user": "ikhaleelem@gmail.com",
                                "title": "test note1",
                                "description": "test description1",
                                "labels": ["label1"],
                                "collaborators": ["ikhaleelem@gmail.com"]
                                }

        self.valid_note_put_data = {'user': "ikhaleelem@gmail.com",
                                    'title': "test note",
                                    'description': "Test description",
                                    'labels': ["label1"],
                                    'collaborators': ["ikhaleelem@gmail.com"]
                                    }
        
        
        self.invalid_note_data = {'user': "ikhale@gmail.com",
                                  'description': "test description1",
                                  'labels': ["label"],
                                  'collaborators': 1,
                                  }
        


class NotesTest(Data):


    def test_given_valid_note_url_for_crud(self):
        self.client.post(self.register_url, self.valid_registration_data, format='json')
        self.client.post(self.label_create_url, self.valid_label_data,format='json')
        self.client.post(self.note_create_url, self.valid_note_data, format='json')
        
        response = self.client.get(self.note_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        response = self.client.post(self.note_create_url, self.valid_note_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put(self.note_update_url, self.valid_note_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.note_update_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)


    def test_given_invalid_note_details_for_crud(self):

        response = self.client.get(self.note_update_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.note_create_url, self.invalid_note_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.note_update_url, self.valid_note_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.note_update_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
