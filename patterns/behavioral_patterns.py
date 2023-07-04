from jsonpickle import dumps, loads

from protasevich_framework.tempalator import render


class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observer = []

    def notify(self):
        for item in self.observer:
            item.update(self)


class SmsNotify(Observer):
    def update(self, subject):
        print(f'SMS оповещение -> студент {subject.students[-1].name} {subject.students[-1].last_name} добавлен на курс {subject.name}')



class EmailNotify(Observer):
    def update(self, subject):
        print(f'Email оповещение -> студент {subject.students[-1].name} {subject.students[-1].last_name} добавлен на курс {subject.name}')


class TemplateView:
    template_name = 'list.html'

    def get_context_data(self):
        return {}

    def get_template_name(self):
        return self.template_name

    def get_template_with_context(self):
        template = self.get_template_name()
        context = self.get_context_data()
        return '200 OK', render(template, **context)

    def __call__(self, request):
        return self.get_template_with_context()


class ListView(TemplateView):
    template_name = 'list.html'
    queryset = []
    context_name = 'objects_name'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_name(self):
        return self.context_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_name = self.get_context_name()
        context = {context_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_object(self, request):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(request)

            return self.get_template_with_context()
        else:
            return super().__call__(request)


class BaseSerialazer:
    def __init__(self, obj):
        self.obj = obj

    def dump(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)

# паттерн стратегия
class ConsoleWrite:
    def write(self, log_message):
        print(log_message)


class FileWrite:
    def write(self, log_message):
        with open('logger.txt', 'a') as f:
            f.write(f'{log_message}\n')
