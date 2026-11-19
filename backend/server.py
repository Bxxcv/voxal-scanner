"""Serve only the VOCXAL demo assets; no scanning or outbound requests."""

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    '/': ('index.html', 'text/html'),
    '/index.html': ('index.html', 'text/html'),
    '/dashboard.html': ('dashboard.html', 'text/html'),
    '/report.html': ('report.html', 'text/html'),
    '/css/style.css': ('css/style.css', 'text/css'),
    '/js/scanner.js': ('js/scanner.js', 'text/javascript'),
    '/js/scenarios.mjs': ('js/scenarios.mjs', 'text/javascript'),
}


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.serve_asset(include_body=True)

    def do_HEAD(self):
        self.serve_asset(include_body=False)

    def do_POST(self):
        self.send_response(HTTPStatus.METHOD_NOT_ALLOWED)
        self.send_header('Allow', 'GET, HEAD')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def serve_asset(self, *, include_body):
        asset = PAGES.get(self.path.partition('?')[0])
        if asset is None:
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        filename, content_type = asset
        try:
            body = (ROOT / filename).read_bytes()
        except OSError as error:
            self.log_error('Unable to read %s: %s', filename, error)
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', f'{content_type}; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy',
                         "default-src 'self'; connect-src 'none'; object-src 'none'; "
                         "base-uri 'none'; form-action 'self'")
        self.end_headers()
        if include_body:
            self.wfile.write(body)


if __name__ == '__main__':
    with ThreadingHTTPServer(('0.0.0.0', 5000), DemoHandler) as server:
        print('VOCXAL demo listening on port 5000', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
