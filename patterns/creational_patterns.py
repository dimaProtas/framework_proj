from copy import deepcopy
import datetime
from quopri import decodestring


class CursesPrototype:
    def clone(self):
        return deepcopy(self)


class Curses(CursesPrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class Interactive(Curses):
    pass


class Record(Curses):
    pass


class CourseFactory:
    types = {
        'interactive': Interactive,
        'record': Record,
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += len(self.category.courses)
        return result


class Engine:
    def __init__(self):
        self.courses = []
        self.categories = []
        self.teacher = []
        self.student = []

    @staticmethod
    def create_user(type_, name, last_name, email, post=None):
        if type_ == 'teacher':
            return Teacher(name, last_name, email, post)
        elif type_ == 'student':
            return Student(name, last_name, email)
        else:
            raise ValueError(f"Invalid user type: {type_}")

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for i in self.categories:
            print('category', i.id)
            if i.id == id:
                return i
        raise Exception(f'Нет такой категории {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_curses(self, name):
        for i in self.courses:
            if i.name == name:
                return i
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decoded_str = decodestring(val_b)
        return val_decoded_str.decode('UTF-8')


class User:
    def __init__(self, name, last_name, email):
        self.name = name
        self.last_name = last_name
        self.email = email


class Teacher(User):
    def __init__(self, name, last_name, email, post):
        super().__init__(name, last_name, email)
        self.post = post



class Student(User):
    pass


class UserFactory:
    types = {
        'teacher': Teacher,
        'student': Student,
    }

    @classmethod
    def create(cls, type_, name, last_name, email, post=None):
        return cls.types[type_](name, last_name, email, post)


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text, additional_info=None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {text}"

        if additional_info:
            log_message += f" - {additional_info}"

        print(log_message)
        with open('logger.txt', 'a') as f:
            f.write(log_message + "\n")
