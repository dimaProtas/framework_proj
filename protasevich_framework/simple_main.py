from protasevich_framework.my_requests import process_get_data, process_form_data


class NotFoundPage:
    def __call__(self, request):
        return '404 Not Found', 'Page not found'


class Aplication:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if not path.endswith('/'):  # обработка наличия (отсутствия) слеша в конце адрес
            path += '/'
        if path in self.routes:
            view = self.routes[path]
        else:
            view = NotFoundPage()

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            request['data'] = process_form_data(environ)

        elif method == 'GET':
            request['request_params'] = process_get_data(environ)

        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


# FakeAplication - фейковый фреймворк, на каждой странице выводит сообщение Fake aplication
class FakeAplication(Aplication):
    def __init__(self, routes, fronts):
        self.aplication = Aplication(routes, fronts)
        super().__init__(routes, fronts)

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Fake aplication']


# DebugAplication - логирующий фреймвор наследуется от основного(выводит принт содержимого enviroment).
class DebugAplication(Aplication):
    def __init__(self, routes, fronts):
        self.aplication = Aplication(routes, fronts)
        super().__init__(routes, fronts)

    def __call__(self, environ, start_response):
        print('Debug Aplication')
        print(environ)
        return self.aplication(environ, start_response)
