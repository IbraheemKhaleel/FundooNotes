"""
Author: Ibraheem Khaleel
Created on: 15th December 2020 
"""
import logging
import os

from django.db.models import Q
from django.utils.decorators import method_decorator
from myfundooNotes.decorators import user_login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import utils
from .models import Note
from .serializers import NoteSerializer

# Create your views here.
from services.cache import Cache

from services.exceptions import LengthError, ValidationError, EmptyFieldError, NoSearchFoundError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s | %(message)s')

file_handler = logging.FileHandler(os.path.abspath("loggers/log_notes.log"))
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

cache = Cache()

class NotesOverview(APIView):
    """
    Created a class for displaying overview of urls using in operations

    """

    def get(self, request):
        """
        Created a method for displaying overview of urls
        @return: All the note and label APIs
        """
        api_urls = {
            'Note-CreateAndRetrieve': '/note/',
            'Note-Update': '/note-update/<int:pk>/',
            'Label-CreateAndRetrieve': '/label/',
            'Label-UpdateAndDelete': '/label-update/<int:pk>/',
            'Pinned Note-List|Detail': '/pinned-note/',
            'Archived Note-List|Detail': '/archived-note/',
            'Trashed Note-List|Detail': '/trashed-note/',
            'Manage-Archive-Note': 'manage-archived-note/<int:pk>/'
        }
        return Response(api_urls)


@method_decorator(user_login_required, name='dispatch')
class ManageNotes(APIView):
    """[allows viewing notes for get and creates new note for post]

    Returns:
        [json]: [list of notes with complete details or creation confirmation and status code]
    """


    def get(self, request, **kwargs):
        """[displays specific note and all notes depends on user input]
        args: kwargs[userid]: user id of the user decoded from token
        Returns:
            Response: status , message and data
            @type: status: Boolean, message:str, data: list
        """

        try:
            current_user = kwargs['userid']
            if kwargs.get('pk'):
                if cache.get_cache(
                        "NOTE_" + str(kwargs.get('pk')) + "_DETAIL") is not None:  # retrieving notes from cache
                    note = cache.get_cache("NOTE_" + str(kwargs.get('pk')) + "_DETAIL")
                    result = utils.manage_response(status=True, message='retrieved successfully', data=note, log=note, logger_obj=logger)
                    return Response(result, status.HTTP_200_OK)
                else:
                    note = Note.objects.get(Q(id=kwargs.get('pk')), Q(is_archived=False), Q(is_trashed=False),
                                            Q(user=current_user) | Q(
                                                collaborators=current_user))  # retrieving data from database
                    serializer = NoteSerializer(note)
                    cache.set_cache("NOTE_" + str(note.id) + "_DETAIL",
                                    str(serializer.data))  # saving notes to redis cache
            else:
                notes = Note.objects.filter(Q(user=kwargs['userid']) | Q(collaborators=kwargs['userid']), Q(is_archived=False)).exclude(
                    is_trashed=True).distinct()
                serializer = NoteSerializer(notes, many=True)

            result = utils.manage_response(status=True, message='retrieved successfully', data=serializer.data,
                                           log=serializer.data, logger_obj=logger)
            return Response(result, status.HTTP_200_OK, content_type='application/json')
        except EmptyFieldError as e:
            result = utils.manage_response(status=False, message='No notes exists', log=str(e),
                                           logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            result = utils.manage_response(status=False, message='Please enter an integer', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Note.DoesNotExist as e:
            result = utils.manage_response(status=False, message='note not found', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def post(self, request, **kwargs):
        """
        A method to post notes of the user
        @param request: title: title of note (mandatory)
                        @type:str
                        description: description the note (mandatory)
                        @type:str
                        collaborators: any collaborator work in same note
                        @type:list
                        labels: label for the note
                        @type:list

        @param kwargs[userid]: user id of the user decoded from token
        @type kwargs[userid]: int
        @return: status, message and status code
        @rtype: status: boolean, message: str
        """
        try:
            data = request.data
            if data is None:
                raise EmptyFieldError('Please fill the fields. Do not leave it empty')
            utils.set_user(request, kwargs['userid'])
            if data.get('collaborators'):
                utils.get_collaborator_list(request)
            if data.get('labels'):
                utils.get_label_list(request)
            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):  # Return a 400 response if the data was invalid.
                serializer.save()
                result = utils.manage_response(status=True, message='created successfully', data=serializer.data,
                                               log=serializer.data, logger_obj=logger)
                return Response(result, status.HTTP_201_CREATED)
            else:
                result = utils.manage_response(status=False, message=serializer.errors, log=serializer.errors, logger_obj=logger)
                return Response(result, status.HTTP_400_BAD_REQUEST)
        except LengthError as e:
            result = utils.manage_response(status=False, message='title length should be between 3 to 50 characters',
                                           log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            result = utils.manage_response(status=False, message='Please provide valid details',
                                           log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except EmptyFieldError as e:
            result = utils.manage_response(status=False, message='Empty field. Type something', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong. Try again', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, **kwargs):
        """
        A method to post notes of the user
        @param request: title: title of note (mandatory)
                        @type:str
                        description: description the note (mandatory)
                        @type:str
                        collaborators: any collaborator work in same note
                        @type:list
                        labels: label for the note
                        @type:list
        @param pk: primary key of the note id
        @type:int
        @param kwargs[userid]: user id of the user decoded from token
        @type kwargs[userid]: int

        @return: status, message,data and status code
        @rtype: status: boolean, message: str, data:list
        """
        try:
            data = request.data
            if data.get('collaborators'):
                utils.get_collaborator_list(request)
            if data.get('labels'):
                utils.get_label_list(request)

            note = Note.objects.get(Q(id=pk), Q(is_trashed=False),
                                    Q(user=kwargs['userid']))
            serializer = NoteSerializer(note, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                cache.set_cache("NOTE_" + str(note.id) + "_DETAIL", str(serializer.data))
            else:
                result = utils.manage_response(status=False, message=serializer.errors, log=serializer.errors, logger_obj=logger)
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result = utils.manage_response(status=True, message='updated successfully', data=serializer.data,
                                           log=serializer.data, logger_obj=logger)
            return Response(result, status.HTTP_200_OK)
        except ValidationError as e:
            result = utils.manage_response(status=False, message='Please enter proper details for each field', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            result = utils.manage_response(status=False, message='Please enter an integer', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Note.DoesNotExist as e:
            print(e)
            result = utils.manage_response(status=False, message='note not found', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:

            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, **kwargs):
        """[trash deletes existing note]
        Returns:
            [Response]: [confirmation message and status]
        """
        try:
            note = Note.objects.get(id=pk, is_trashed=False, user=kwargs['userid'])
            note.trashed()
            cache.delete_cache("NOTE_" + str(note.id) + "_DETAIL")
            result = utils.manage_response(status=True, message='note trashed successfully',
                                           log='note trashed successfully', logger_obj=logger)
            return Response(result, status.HTTP_204_NO_CONTENT)

        except Note.DoesNotExist as e:
            result = utils.manage_response(status=False, message='note not found', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)


@method_decorator(user_login_required, name='dispatch')
class ManageArchivedNote(APIView):
    """
    [shows all archived notes or specific note if pk is passed]

    """

    def get(self, request, **kwargs):
        """[displays archived notes on user input]
        args: kwargs[userid]: user id of the user decoded from token
        Returns:
            Response: status , message and data
            @type: status: Boolean, message:str, data: list
        """
        try:
            current_user = kwargs['userid']
            if kwargs.get('pk'):
                note = Note.objects.get(Q(id=kwargs.get('pk')), Q(is_archived=True), Q(is_trashed=False),
                                        Q(user=current_user) | Q(collaborators=current_user))
                serializer = NoteSerializer(note)
            else:
                notes = Note.objects.filter(Q(user=kwargs['userid']) | Q(collaborators=kwargs['userid']),
                                            is_archived=True, is_trashed=False)
                serializer = NoteSerializer(notes, many=True)

            result = utils.manage_response(status=True, message='retrieved successfully', data=serializer.data,
                                           log=serializer.data, logger_obj=logger)
            return Response(result, status.HTTP_200_OK)
        except Note.DoesNotExist as e:
            result = utils.manage_response(status=False, message='note not found', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            result = utils.manage_response(status=False, message='Please enter an integer', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)


@method_decorator(user_login_required, name='dispatch')
class ManagePinnedNotes(APIView):
    """
    [shows all pinned notes or specific note if pk is passed]

    """

    def get(self, request, **kwargs):
        """[displays pinned notes and all notes depends on user input]
        args: kwargs[userid]: user id of the user decoded from token
        Returns:
            Response: status , message and data
            @type: status: Boolean, message:str, data: list
        """
        try:
            current_user = kwargs['userid']
            if kwargs.get('pk'):
                note = Note.objects.get(Q(id=kwargs.get('pk')), Q(is_archived=False), Q(is_trashed=False),
                                        Q(is_pinned=True),
                                        Q(user=current_user) | Q(collaborators=current_user))
                serializer = NoteSerializer(note)
                type(serializer.data)
            else:
                notes = Note.objects.filter(Q(user=kwargs['userid']) | Q(collaborators=kwargs['userid']),
                                            is_trashed=False).exclude(
                    is_archived=True).exclude(is_pinned=False)
                serializer = NoteSerializer(notes, many=True)

            result = utils.manage_response(status=True, message='retrieved successfully', data=serializer.data,
                                           log=serializer.data, logger_obj=logger)
            type(serializer.data)
            return Response(result, status.HTTP_200_OK)
        except Note.DoesNotExist as e:
            result = utils.manage_response(status=False, message='note not found', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            result = utils.manage_response(status=False, message='Please enter an integer', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)


@method_decorator(user_login_required, name='dispatch')
class ManageTrashedNotes(APIView):
    """
    [shows all trashed notes or specific note if pk is passed ]
    soft deletes the trashed note
    """

    def get(self, request, **kwargs):
        """[displays trashed note note on user input]
        args: kwargs[userid]: user id of the user decoded from token
        Returns:
            Response: status , message and data
            @type: status: Boolean, message:str, data: list
        """
        try:
            current_user = kwargs['userid']
            if kwargs.get('pk'):
                note = Note.objects.get(id=kwargs.get('pk'), is_trashed=True, user=current_user)
                serializer = NoteSerializer(note)

            else:
                notes = Note.objects.filter(user=kwargs['userid'], is_trashed=True)
                serializer = NoteSerializer(notes, many=True)

            result = utils.manage_response(status=True, message='retrieved successfully', data=serializer.data,
                                           log=serializer.data, logger_obj=logger)
            return Response(result, status.HTTP_200_OK)
        except TypeError as e:
            result = utils.manage_response(status=False, message='Please enter an integer', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Note.DoesNotExist as e:
            result = utils.manage_response(status=False, message='note not found', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, **kwargs):
        """[soft deletes trashed note]
        Returns:
            [Response]: [confirmation message and status]
        """
        try:
            note = Note.objects.get(id=pk, is_archived=False, is_trashed=True, user=kwargs['userid'])

            note.soft_delete()
            result = utils.manage_response(status=True, message='note deleted successfully',
                                           log=('deleted note with id: {}'.format(pk)), logger_obj=logger)
            return Response(result, status.HTTP_204_NO_CONTENT)
        except TypeError as e:
            result = utils.manage_response(status=False, message='Please enter an integer', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)

        except Note.DoesNotExist as e:
            result = utils.manage_response(status=False, message='note not found', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)


@method_decorator(user_login_required, name='dispatch')
class SearchNote(APIView):
    """
    Created a class to search a particular note
    """

    def get(self, request, **kwargs):
        """
        created a method ;to obtain the notes,if searched by any of its words inside it.
        @param kwargs: user id of the respective user
        @return: The notes with the searched text
        @rtype: string
        """
        try:
            current_user = kwargs['userid']
            search_terms = request.query_params.get('search_term')
            if search_terms is '':
                raise EmptyFieldError('Please enter a seach term')
            search_term_list = search_terms.split(' ')

            notes = Note.objects.filter(Q(user=current_user) | Q(collaborators=current_user), is_trashed=False,
                                        is_deleted=False)
            search_query = Q(title__icontains=search_term_list[0]) | Q(description__icontains=search_term_list[0])
            for term in search_term_list[1:]:
                search_query.add((Q(title__icontains=term) | Q(description__icontains=term)),
                                 search_query.connector)
            notes = notes.filter(search_query)
            serializer = NoteSerializer(notes, many=True)
            if serializer.data.__eq__([]):
                raise NoSearchFoundError('The value you searched have no match in title and description')
            result = utils.manage_response(status=True, message='retrieved notes on the basis of search terms',
                                           data=serializer.data,
                                           log='retrieved searched note', logger_obj=logger)
            return Response(result, status.HTTP_200_OK)
        except NoSearchFoundError as e:
            result = utils.manage_response(status=False, message='Your searched note is nowhere in the notes',
                                           log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist as e:
            result = utils.manage_response(status=False, message='note not found', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e), logger_obj=logger)
            return Response(result, status.HTTP_400_BAD_REQUEST)
