import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

from backend.server import DemoHandler


class DemoServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), DemoHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def request(self, method, path):
        with self.subTest(method=method, path=path):
            connection = HTTPConnection(*self.server.server_address, timeout=3)
            self.addCleanup(connection.close)
            connection.request(method, path)
            response = connection.getresponse()
            return response.status, response.getheader('Content-Type'), response.read()

    def test_demo_pages_and_assets_are_served(self):
        for path, media_type in [
            ('/', 'text/html'), ('/dashboard.html', 'text/html'),
            ('/report.html?scenario=catalog', 'text/html'),
            ('/css/style.css', 'text/css'), ('/js/scanner.js', 'text/javascript'),
            ('/js/scenarios.mjs', 'text/javascript'),
        ]:
            status, content_type, body = self.request('GET', path)
            self.assertEqual(status, 200)
            self.assertIn(content_type.split(';')[0], {media_type, 'application/javascript'} if media_type == 'text/javascript' else {media_type})
            self.assertTrue(body)

    def test_backend_and_legacy_api_are_not_exposed(self):
        for path in ('/backend/server.py', '/backend/scanner-engine.py', '/.git/config',
                     '/js/', '/api/scan', '/js/../backend/server.py', '//backend/server.py'):
            self.assertEqual(self.request('GET', path)[0], 404)
        self.assertEqual(self.request('POST', '/api/scan')[0], 405)

    def test_head_does_not_return_body(self):
        self.assertEqual(self.request('HEAD', '/')[-1], b'')
