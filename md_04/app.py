from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import pprint


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/contact':
            self.send_html_file('contact.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-length']))
        pprint.pprint(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        pprint.pprint(data_parse)
        data_dict = {
            key: value for key, value in [el.split('=') for el in data_parse.split('&')]
        }
        pprint.pprint(data_dict)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
    
    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Conent-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())
    
    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt: 
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/palin')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    
def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 8000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()