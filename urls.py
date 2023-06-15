from view import Index, abc_view, Obout, Contact, Programs

routes = {
    '/': Index(),
    '/abc/': abc_view,
    '/obout/': Obout(),
    '/contact/': Contact(),
    '/programs/': Programs(),
}


def secret_front(request):
    request['secret'] = 'some_secret'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]
