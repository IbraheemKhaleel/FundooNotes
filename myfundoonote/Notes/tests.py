from rest_framework import status
from rest_framework.test import APITestCase


class Data(APITestCase):
    def setUp(self):
        self.register_url = 'http://127.0.0.1:8000/register/'
        self.note_get_post_url = 'http://127.0.0.1:8000/note/'
        self.note_put_delete_url = 'http://127.0.0.1:8000/note-update/1/'

        self.valid_note_data = {'user': [ibrahee@gmail.com],
                                'title': "my testing note",
                                'description': "Need a change",
                                'labels': "Third Note",
                                'collaborators': [ibrahee@gmail.com],
                                }
        self.valid_note_put_data = {'user': 1,
                                    'title': "this is not a demo note",
                                    'description': "Need a change",
                                    'labels': "second note",
                                    'collaborators': [1],
                                    }
        self.invalid_note_data = {'user': 1,
                                  'description': "Need a change",
                                  'labels': "Third Note",
                                  'collaborators': [1],
                                  }
        self.valid_registration_data =  {'first_name': "Ibraheeem",
                                        'last_name': "Khaleeel",
                                        'email': "ibrahee@gmail.com",
                                        'user_name': "ibrahikhaleel",
                                        'password': "itisinotmypassport"}


class NotesTest(Data):
    def test_given_valid_note_url_for_crud(self):
        life = self.client.post(self.register_url, self.valid_registration_data, format='json')
        print(life)
        yes = self.client.post(self.note_get_post_url, self.valid_note_data, format='json')
        print(yes)

        response = self.client.get(self.note_put_delete_url, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        response = self.client.put(self.note_put_delete_url, self.valid_note_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.note_put_delete_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_invalid_note_details_for_crud(self):
        response = self.client.post(self.note_get_post_url, self.invalid_note_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.note_put_delete_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.note_put_delete_url, self.valid_note_put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.note_put_delete_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
