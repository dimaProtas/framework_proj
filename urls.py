from view import Index, Obout, Contact, Programs, Category, Courses, CopyCourses, Users

routes = {
    '/': Index(),
    '/obout/': Obout(),
    '/contact/': Contact(),
    '/programs/': Programs(),
    '/category/': Category(),
    '/courses/': Courses(),
    '/copy-course/': CopyCourses(),
    '/users/': Users(),
}


def secret_front(request):
    request['secret'] = 'some_secret'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]
