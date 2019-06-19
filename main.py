from api import AmazonApi
import json
from urllib.parse import urlparse, parse_qs, quote
import http.server
import socketserver

class ServerHandler(http.server.BaseHTTPRequestHandler):

    def _set_headers(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers(200)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/':
            query_components = parse_qs(url.query)
            if not 'article' in query_components:
                self._set_headers(400)
                self.wfile.write(str.encode(json.dumps({'error': "Missing parameter 'article'"})))
                return

            articleId = query_components['article'][0]

            amazon = AmazonApi()
            article = amazon.getArticleInformation("https://www.amazon.de/dp/" + quote(articleId))

            if(article == None):
                self._set_headers(404)
                self.wfile.write(str.encode(json.dumps({'error': "This article does not exist"})))
            else:
                self._set_headers(200)
                self.wfile.write(str.encode(json.dumps(article.__dict__)))

PORT = 8081
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), ServerHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()