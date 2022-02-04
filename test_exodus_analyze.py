import unittest

from exodus_analyze import get_ignore_list


class TestGetIgnoreList(unittest.TestCase):

    def test_returns_empty_list_if_none(self):
        given_arg = None
        expected_list = ([], '')

        self.assertEqual(get_ignore_list(given_arg), expected_list)

    def test_returns_list_of_one_id_if_set(self):
        given_arg = '23'
        expected_list = ([23], '')

        self.assertEqual(get_ignore_list(given_arg), expected_list)

    def test_returns_list_of_two_ids_if_set(self):
        given_arg = '23,35'
        expected_list = ([23, 35], '')

        self.assertEqual(get_ignore_list(given_arg), expected_list)

    def test_returns_error_if_wrong_separator(self):
        given_arg = '23;35'
        expected_list = ([], 'incorrect ignore argument')

        self.assertEqual(get_ignore_list(given_arg), expected_list)

    def test_returns_error_if_wrong_argument_format(self):
        given_arg = 'wrongargument'
        expected_list = ([], 'incorrect ignore argument')

        self.assertEqual(get_ignore_list(given_arg), expected_list)
