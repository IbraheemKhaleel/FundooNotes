"""
Test Models
"""
import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestNote:
    def test_init(self):
        note_obj = mixer.blend('Notes.Note')
        assert note_obj.pk == 1, 'Should save an instance'
