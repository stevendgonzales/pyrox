import unittest
import pyrox.http as http
import pyrox.http.filtering as http_filtering
from pyrox.stock_filters.simple import SimpleFilter


class WhenFuncTestingSimpleFilter(unittest.TestCase):
    def setUp(self):
        self.req_message = http.HttpRequest()
        self.req_message.url = 'http://127.0.0.1'
        self.req_message.method = 'GET'
        self.req_message.version = "1.0"
        self.simple_filter = SimpleFilter()

    def test_simple_filter_returns_reject_action(self):
        returned_action = self.simple_filter.on_request(self.req_message)
        self.assertEqual(returned_action.kind, http_filtering.REJECT)

    def test_simple_filter_returns_pass_action(self):
        auth_header = self.req_message.header(name="user-agent")
        auth_header.values.append('Unittest HTTP Request')
        returned_action = self.simple_filter.on_request(self.req_message)
        self.assertEqual(returned_action.kind, http_filtering.NEXT_FILTER)


if __name__ == '__main__':
    unittest.main()
