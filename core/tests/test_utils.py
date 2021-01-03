from random import randrange
from django.test import TestCase
from core.utils import FileUtils
from core.enums import FileSize


class TestFileUtils(TestCase):

    def test_convert_to_byte(self):
        for enum in FileSize:
            number = randrange(20)
            byte_value = FileUtils.convert_to_byte(number,enum.name)
            self.assertGreaterEqual(byte_value,number)
