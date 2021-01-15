"""
Test Models
"""
import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestLabels:
    def test_init(self):
        label_obj = mixer.blend('labels.Label')
        assert label_obj.pk == 1, 'Should save an instance'