import os
import socketserver
import traceback
import http.server
from urllib.parse import urlsplit

import metrics

area_id = os.getenv('area_id')
assert area_id and area_id.isdigit(), 'Env var area_id is missing or not a number'
area_id = int(area_id)

station_id = os.getenv('station_id')
assert station_id, 'Env var station_id is missing'

class HttpHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def send(self, content: str, code: int, mime: str):
        content = content.encode('utf8')
        self.send_response(code)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        try:
            url = urlsplit(self.path.strip() or '/')
            if url.path == '/metrics':
                return self.send(metrics.generate(area_id, station_id), code=200, mime='text/plain; version=0.0.4')
            return self.send('404 not found', code=404, mime='text/plain')
        except Exception as e:
            traceback.print_exc()
            return self.send(str(e), code=500, mime='text/plain')


class HttpServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True


server = HttpServer(('', 8080), HttpHandler)
print('visit: http://localhost:8080/metrics')
server.serve_forever()
