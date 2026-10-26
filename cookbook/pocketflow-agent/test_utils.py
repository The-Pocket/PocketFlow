import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import requests

from utils import search_web_brave


class TestBraveSearch(unittest.TestCase):
    def test_formats_successful_results(self):
        response = requests.Response()
        response.status_code = 200
        response._content = (
            b'{"web":{"results":[{"title":"Example","url":"https://example.com",'
            b'"description":"A search result"}]}}'
        )
        with patch('requests.sessions.Session.send', return_value=response):
            self.assertEqual(
                search_web_brave('example'),
                'Title: Example\nURL: https://example.com\nDescription: A search result',
            )

    def test_preserves_special_characters_in_query(self):
        query = 'C++ & C# examples? language=中文'
        response = requests.Response()
        response.status_code = 200
        response._content = b'{"web":{"results":[]}}'
        with patch('requests.sessions.Session.send', return_value=response) as send:
            self.assertEqual(search_web_brave(query), '')

        request = send.call_args.args[0]
        self.assertEqual(parse_qs(urlsplit(request.url).query), {'q': [query]})

    def test_propagates_http_errors_before_parsing_response(self):
        for status in (401, 429, 500):
            with self.subTest(status=status):
                response = requests.Response()
                response.status_code = status
                response._content = b'Not a JSON response'
                with patch('requests.sessions.Session.send', return_value=response):
                    with self.assertRaises(requests.HTTPError) as raised:
                        search_web_brave('example')
                self.assertIs(raised.exception.response, response)


if __name__ == '__main__':
    unittest.main()
