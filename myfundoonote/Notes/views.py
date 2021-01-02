"""
Author: Ibraheem Khaleel
Created on: 15th December 2020 
"""

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


class NotesOverview(APIView):
    """
    Created a class for displaying overview of urls using in operations

    """
    
    def get(self , request):
        """
        Created a method for displaying overview of urls 

        """
        api_urls = {    
            'Note-CreateAndRetrieve':'/note/',
            'Note-Update':'/note-update/<int:pk>/',
            'Label-CreateAndRetrieve': '/label/',
            'Label-UpdateAndDelete':'/label-update/<int:pk>/',
            'Pinned Note-List|Detail': '/pinned-note/',
            'Archived Note-List|Detail': '/archived-note/',
            'Trashed Note-List|Detail': '/trashed-note/',
            'Manage-Archive-Note' :'manage-archived-note/<int:pk>/'
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
        Returns:
            [Response]: [notes result data and status]
        """
        try:
            current_user = kwargs['userid']
            cache = Cache()
            if kwargs.get('pk'):
                if cache.get_cache("NOTE_" + str(kwargs.get('pk')) + "_DETAIL") is not None: #retrieving notes from cache
                    note = cache.get_cache("NOTE_" + str(kwargs.get('pk')) + "_DETAIL")
                    result = utils.manage_response(status=True, message='retrieved successfully', data=note, log=note)
                    return Response(result, status.HTTP_200_OK)
                else:
                    note = Note.objects.get(Q(id=kwargs.get('pk')), Q(is_deleted=False),
                                            Q(user=current_user) | Q(collaborators=current_user)) #rertieving data from database
                    serializer = NoteSerializer(note)
                    cache.set_cache("NOTE_" + str(note.id) + "_DETAIL", str(serializer.data)) #sasving notes to redis cache
            else:
                notes = Note.objects.filter(Q(user=kwargs['userid']) | Q(collaborators=kwargs['userid'])).exclude(
                    is_deleted=True)
                serializer = NoteSerializer(notes, many=True)

            result = utils.manage_response(status=True, message='retrieved successfully', data=serializer.data,
                                           log=serializer.data)
            return Response(result, status.HTTP_200_OK)

        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e))
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def post(self, request, **kwargs):
        """[creates new note]
        Returns:
            [Response]: [result data and status]
        """
        try:
            data = request.data
            utils.set_user(request, kwargs['userid'])
            if data.get('collaborators'):
                utils.get_collaborator_list(request)
            if data.get('labels'):
                utils.get_label_list(request)

            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):  # Return a 400 response if the data was invalid.
                serializer.save()
                result = utils.manage_response(status=True, message='created successfully', data=serializer.data,
                                               log=serializer.data)
                return Response(result, status.HTTP_201_CREATED)
            else:
                result = utils.manage_response(status=False, message=serializer.errors, log=serializer.errors)
                return Response(result, status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist as e:
            result = utils.manage_response(status=False, message='note not found', log=str(e))
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message=str(e), log=str(e))
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, **kwargs):
        """[updates existing note]
        Returns:
            [Response]: [updated details and status]
        """
        try:

            data = request.data
            if data.get('collaborators'):
                utils.get_collaborator_list(request)
            if data.get('labels'):
                utils.get_label_list(request)

            note = Note.objects.get(Q(id=pk), Q(is_deleted=False),
                                    Q(user=kwargs['userid']))

            serializer = NoteSerializer(note, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                result = utils.manage_response(status=False, message=serializer.errors, log=serializer.errors)
                return Response(result, status.HTTP_400_BAD_REQUEST)

            result = utils.manage_response(status=True, message='updated successfully', data=serializer.data,
                                           log=serializer.data)
            return Response(result, status.HTTP_200_OK)

        except Note.DoesNotExist as e:

            result = utils.manage_response(status=False, message='note not found', log=str(e))
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:

            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e))
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, **kwargs):
        """[soft deletes existing note]
        Returns:
            [Response]: [confirmation message and status]
        """
        try:
            note = Note.objects.get(Q(id=pk), Q(is_deleted=False), Q(user=kwargs['userid']))

            note.soft_delete()
            result = utils.manage_response(status=True, message='note deleted successfully',
                                           log=('deleted note with id: {}'.format(pk)))
            return Response(result, status.HTTP_204_NO_CONTENT)

        except Note.DoesNotExist as e:
            result = utils.manage_response(status=False, message='note not found', log=str(e))
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e))
            return Response(result, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, **kwargs):
        """[updates existing note]
        Returns:
            [Response]: [updated details and status]
        """
        try:
            data = request.data
            if data.get('collaborators'):
                utils.get_collaborator_list(request)
            if data.get('labels'):
                utils.get_label_list(request)

            note = Note.objects.get(Q(id=pk), Q(is_deleted=False), Q(user=kwargs['userid']))
            serializer = NoteSerializer(note, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                result = utils.manage_response(status=False, message=serializer.errors, log=serializer.errors)
                return Response(result, status.HTTP_400_BAD_REQUEST)
            result = utils.manage_response(status=True, message='updated successfully', data=serializer.data, log=serializer.data)
            return Response(result, status.HTTP_200_OK)

        except Note.DoesNotExist as e:
            result = utils.manage_response(status=False, message='note not found', log=str(e))
            return Response(result, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e))
            return Response(result, status.HTTP_400_BAD_REQUEST)

@method_decorator(user_login_required, name='dispatch')
class ManageArchivedNote(APIView):
    """[shows all notes or specific note if pk is passed]

    Args:
        APIView ([type]): [description]
    """

    def get(self, request, **kwargs):
        """[shows all notes or specific note if pk is passed]

        Args:
            request ([type]): [description]
            pk ([int]): [id of required note]
        """
        try:
            current_user = kwargs['userid']
            if kwargs.get('pk'):
                note = Note.objects.get(Q(id=kwargs.get('pk')), Q(is_deleted=False), Q(is_archived=True),
                                        Q(user=current_user) | Q(collaborators=current_user))
                serializer = NoteSerializer(note)
            else:
                notes = Note.objects.filter(Q(user=kwargs['userid']) | Q(collaborators=kwargs['userid'])).exclude(
                    is_deleted=True).exclude(is_archived=False)
                serializer = NoteSerializer(notes, many=True)

            result = utils.manage_response(status=True, message='retrieved successfully', data=serializer.data,
                                           log=serializer.data)
            return Response(result, status.HTTP_200_OK)

        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e))
            return Response(result, status.HTTP_400_BAD_REQUEST)


@method_decorator(user_login_required, name='dispatch')
class ManagePinnedNotes(APIView):
    """[shows all pinned notes or specific note if pk is passed]

    Args:
        APIView ([type]): [description]
    """

    def get(self, request, **kwargs):
        """[shows all pinned notes or specific note if pk is passed]

        Args:
            request ([type]): [description]
            pk ([int]): [id of required note]
        """
        try:
            current_user = kwargs['userid']
            if kwargs.get('pk'):
                note = Note.objects.get(Q(id=kwargs.get('pk')), Q(is_deleted=False), Q(is_pinned=True),
                                        Q(user=current_user) | Q(collaborators=current_user))
                serializer = NoteSerializer(note)

            else:
                notes = Note.objects.filter(Q(user=kwargs['userid']) | Q(collaborators=kwargs['userid'])).exclude(
                    is_deleted=True).exclude(is_pinned=False)
                serializer = NoteSerializer(notes, many=True)

            result = utils.manage_response(status=True, message='retrieved successfully', data=serializer.data,
                                           log=serializer.data)
            return Response(result, status.HTTP_200_OK)

        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e))
            return Response(result, status.HTTP_400_BAD_REQUEST)


@method_decorator(user_login_required, name='dispatch')
class ManageTrashedNotes(APIView):
    """[shows all trashed notes or specific note if pk is passed]

    Args:
        APIView ([type]): [description]
    """

    def get(self, request, **kwargs):
        """[shows all trashed notes or specific note if pk is passed]

        Args:
            request ([type]): [description]
            pk ([int]): [id of required note]
        """
        try:
            current_user = kwargs['userid']
            if kwargs.get('pk'):
                note = Note.objects.get(Q(id=kwargs.get('pk')), Q(is_deleted=True), Q(user=current_user))
                serializer = NoteSerializer(note)

            else:
                notes = Note.objects.filter(Q(user=kwargs['userid'])).exclude(is_deleted=False)
                serializer = NoteSerializer(notes, many=True)

            result = utils.manage_response(status=True, message='retrieved successfully', data=serializer.data,
                                           log=serializer.data)
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result = utils.manage_response(status=False, message='Something went wrong.Please try again.', log=str(e))
            return Response(result, status.HTTP_400_BAD_REQUEST)
