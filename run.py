from wsgiref.simple_server import make_server
from protasevich_framework.simple_main import Aplication
from urls import fronts, routes


application = Aplication(routes, fronts)

with make_server('', 8000, application) as httpd:
    print("Server started on port 8000.")
    httpd.serve_forever()
