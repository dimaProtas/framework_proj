from wsgiref.simple_server import make_server
from protasevich_framework.simple_main import Aplication, FakeAplication, DebugAplication
from urls import fronts
from view import routes


application = Aplication(routes, fronts)

with make_server('', 8000, application) as httpd:
    server_address = 'http://127.0.0.1:8000'
    print(f"Server started on address {server_address}.")

    httpd.serve_forever()

