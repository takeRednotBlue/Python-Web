"""
Ваша мета реалізувати найпростіший вебзастосунок. За основу взяти наступні файли.

За аналогією з розглянутим прикладом у конспекті, створіть вебзастосунок з маршрутизацією для двох html сторінок: index.html та message.html.

Також:

    Обробіть під час роботи застосунку статичні ресурси: style.css, logo.png;
    Організуйте роботу з формою на сторінці message.html;
    У разі виникнення помилки 404 Not Found повертайте сторінку error.html
    Ваш застосунок працює на порту 3000

Для роботи з формою створіть Socket сервер на порту 5000. Алгоритм роботи такий. Ви вводите дані у форму, вони потрапляють у ваш вебзастосунок, 
який пересилає його далі на обробку за допомогою socket (протокол UDP) Socket серверу. Socket сервер перетворює отриманий байт-рядок у словник і 
зберігає його в json файл data.json в папку storage.

Формат запису файлу data.json наступний:

{
  "2022-10-29 20:20:58.020261": {
    "username": "krabaton",
    "message": "First message"
  },
  "2022-10-29 20:21:11.812177": {
    "username": "Krabat",
    "message": "Second message"
  }
}

Де ключ кожного повідомлення - це час отримання повідомлення: datetime.now(). Тобто кожне нове повідомлення від вебзастосунку дописується у файл 
storage/data.json з часом отримання.

Використовуйте для створення вашого вебзастосунку один файл main.py. Запустіть HTTP сервер і Socket сервер у різних потоках.

Це додаткове завдання і його можна не виконувати для здачі цього домашнього завдання.

    Створіть Dockerfile та запустіть ваш застосунок як Docker-контейнер
    За допомогою механізму volumes, зберігайте дані з storage/data.json не всередині контейнера
    
    docker build . -t maksymklym/test-web-servers
    docker run -d -p 3000:3000 -v /home/maksymklym/Documents/storage:/storage maksymklym/test-web-servers
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from threading import Thread
import urllib.parse
import pathlib
import mimetypes
import pprint
import socket
import json

UDP_IP = '127.0.0.1'
UDP_PORT = 5000

TCP_IP = ''
TCP_PORT = 3000

DATA_DIR = pathlib.Path('/') / 'storage'
DATA_FILE = DATA_DIR / 'data.json'

# if not DATA_FILE.exists():
#     with open(DATA_FILE, 'w') as fd:
#         json.dump({}, fd)


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        ''' Handles GET request'''
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/massage':
            self.send_html_file('massage.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self) -> None:
        ''' Handles POST request'''
        data = self.rfile.read(int(self.headers['Content-length']))
        pprint.pprint(data)
        send_data_UDP(data, UDP_IP, UDP_PORT)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
    
    def send_html_file(self, filename: pathlib.Path, status=200) -> None:
        '''Sends html file as response to the browser'''
        self.send_response(status)
        self.send_header('Conent-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())
    
    def send_static(self) -> None:
        '''Handles static resources'''
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt: 
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/palin')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def process_data(data: bytes) -> dict:
    '''Proceses data aquired by POST request and returns dict object
    to be written to json file'''
    data_parse = urllib.parse.unquote_plus(data.decode())
    pprint.pprint(data_parse)
    data_dict = {
        key: value for key, value in [el.split('=') for el in data_parse.split('&')]
    }
    data_obj = {str(datetime.now()): data_dict}
    return data_obj


def save_to_JSON(data: dict, filename: pathlib.Path) -> None:
    '''Saves data to json file. Handles cases when file exists and have to append 
    data object to larger json object'''
    if filename.exists():
        with open(filename, 'r+') as fd:
            storage_data = json.load(fd)
            storage_data.update(data)
            fd.seek(0)
            json.dump(storage_data, fd, indent=4)
    else:            
        with open(filename, 'w') as fd:
            json.dump(data, fd, indent=4)
 

def send_data_UDP(data: bytes, ip: str, port: int) -> None:
    '''Sends data to UDP server'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.sendto(data, server)
    print(f'Send data: {data} to server: {server}')
    response, address = sock.recvfrom(1024)
    print(f'Response data: {response.decode()} from address: {address}')
    sock.close()


def run_server_UDP() -> None:
    '''Runs UDP server'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    filename = DATA_FILE
    server = UDP_IP, UDP_PORT
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(f'Received data: {data.decode()} from: {address}')

            ready_data = process_data(data)
            save_to_JSON(ready_data, filename)
            response = 'Data was successfully saved'
            sock.sendto(response.encode(), address)
            print(f'Send data: {response} to: {address}')
            
    except KeyboardInterrupt:
        print('Destroy server')
    finally:
        sock.close()


def run_web_server(server_class=HTTPServer, handler_class=HttpHandler) -> None:
    '''Runs HTTP server by default'''
    server_address = TCP_IP, TCP_PORT
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()



if __name__ == '__main__':
    http_server = Thread(target=run_web_server)
    udp_server = Thread(target=run_server_UDP)
    http_server.start()
    udp_server.start()
    http_server.join()
    udp_server.join()