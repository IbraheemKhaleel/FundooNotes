"""
Test Models
"""
import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestmyfundooNotes:
    def test_init(self):
        note_obj = mixer.blend('myfundooNotes.User')
        assert note_obj.pk == 1, 'Should save an instance'