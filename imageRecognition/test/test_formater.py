
import pytest
from os import path, remove
from imageRecognition.out import formater

class TestFormater(object):

    def test_format_match(self):
        simple_result = [(["yes"],["no"], 0),
                         (["yes"],["yes"], 100)]
        sample_path = "./result.txt"
        formater.format_match(simple_result, sample_path)

        assert path.isfile(sample_path)
        assert path.getsize(sample_path) > 0
        remove(sample_path)

    def test_format_template(self):
        simple_result = ["yes", "yes", "no"]
        sample_path = "./result.txt"
        formater.format_template(simple_result, sample_path)

        assert path.isfile(sample_path)
        assert path.getsize(sample_path) > 0
        remove(sample_path)

    def test_format_hashing(self):
        simple_result = [(["yes"], ["no"]),
                         (["yes"], ["yes"])]
        sample_path = "./result.txt"
        formater.format_hashing(simple_result, sample_path)

        assert path.isfile(sample_path)
        assert path.getsize(sample_path) > 0
        remove(sample_path)
