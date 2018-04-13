
import pytest
from os import path, remove
from imageRecognition.out import formater

class TestFormater(object):

    def test_format_result(self):
        simple_result = [(["yes"],["no"], 0),
                         (["yes"],["yes"], 100)]
        sample_path = "./"
        filename = formater.get_resultfilename()
        formater.format_result(simple_result, sample_path)

        file_path = path.join(sample_path, filename)

        assert path.isfile(file_path)
        assert path.getsize(file_path) > 0

        remove(file_path)
