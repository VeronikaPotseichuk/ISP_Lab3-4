import pytest 
from mixer.backend.django import mixer 

pytestmark = pytest.mark.django_db  # This is put here so that we can save to the database otherwise it will fail because tests are not written to the database. 
class TestPost:
    def test_init(self):
        obj = mixer.blend('courses.Subject')
        assert obj.pk == 1, 'Should create a Post instance'