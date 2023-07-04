from abc import ABC, abstractmethod
from copy import deepcopy
import datetime
from quopri import decodestring
from patterns.behavioral_patterns import Subject, ConsoleWrite, FileWrite


Subject = Subject


class User:
    def __init__(self, name, last_name, birthdate, email, password):
        self.name = name
        self.last_name = last_name
        self.birthdate = birthdate
        self.email = email
        self.password = password


class Teacher(User):
    auto_id = 0

    def __init__(self, name, last_name, birthdate, email, password):
        self.id = Teacher.auto_id
        Teacher.auto_id += 1
        super().__init__(name, last_name, birthdate, email, password)



class Student(User):
    auto_id = 0

    def __init__(self, name, last_name, birthdate, email, password):
        self.id = Student.auto_id
        Student.auto_id += 1
        self.courses = []
        super().__init__(name, last_name, birthdate, email, password)


class UserFactory:
    types = {
        'teacher': Teacher,
        'student': Student,
    }

    @classmethod
    def create(cls, type_, name, last_name, email, birthdate, password):
        return cls.types[type_](name, last_name, birthdate, email, password)



class CursesPrototype:
    def clone(self):
        return deepcopy(self)


class Curses(CursesPrototype, Subject):
    auto_id = 0

    def __init__(self, name, category):
        self.id = Curses.auto_id
        Curses.auto_id += 1
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        Subject.notify(self)


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

    @classmethod
    def set_course_type(cls, type_, course_type):
        cls.types[type_] = course_type


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

    def redact_course(self, id_course, name, category_name, type_course):
        for item in self.courses:
            if item.id == id_course:
                item.name = name
                item.category.courses.remove(item)
                new_category = None
                for cat in self.categories:
                    if cat.name == category_name:
                        new_category = cat
                        break
                if new_category is None:
                    raise Exception(f"Категория с именем {category_name} не найдена")

                item.category = new_category
                item.category.courses.append(item)
                item.__class__ = CourseFactory.types[type_course]
                return

        raise Exception(f"Курс с идентификатором {id_course} не найден")

    def get_student(self, name) -> Student:
        for item in self.student:
            if item.name == name:
                return item

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

    def find_course_by_id(self, id):
        for i in self.courses:
            print(i.id)
            if i.id == id:
                return i
        raise Exception(f'Нет такого курса -> {id}')

    def find_student_by_id(self, id):
        for i in self.student:
            if i.id == id:
                return i
        raise Exception(f'Нет пользователя с id={id}')

    def find_teacher_by_id(self, id):
        for i in self.teacher:
            if i.id == id:
                return i
        raise Exception(f'Нет пользователя с id={id}')

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


# Поведенческий паттерн шаблонный метод (поместил в этот файл что бы избежать циклического импарта)
class RegisterUsersTemplate(ABC):
    def register_users(self, request):
        self.process_input(request)
        self.validate_input(request)
        self.create_users(request)
        self.send_confirmation_email(request)

    @abstractmethod
    def process_input(self, request):
        pass

    @abstractmethod
    def validate_input(self, request):
        pass

    @abstractmethod
    def create_users(self, request):
        pass

    @abstractmethod
    def send_confirmation_email(self, request):
        pass


class ProcessInputRegister(RegisterUsersTemplate):
    def __init__(self):
        self.registered_emails = set()

    def process_input(self):
        pass

    def validate_input(self, password, repid_password, email):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

        if password != repid_password:
            raise ValueError("Password and confirmation password do not match")

        if email in self.registered_emails:
            raise ValueError("Email already exists. Please choose a different email.")
        else:
            self.registered_emails.add(email)

    def create_users(self, type_, name, lastname, age, email, password):
        if type_ == 'teacher':
            return Teacher(name, lastname, age, email, password)
        elif type_ == 'student':
            return Student(name, lastname, age, email, password)
        else:
            raise ValueError(f"Invalid user type: {type_}")

    def send_confirmation_email(self, email):
        print(email, '- Вы зарегистрированы')


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

    def __init__(self, name, write=FileWrite()):
        self.name = name
        self.write = write

    def log(self, text, additional_info=None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {text}"

        if additional_info:
            log_message += f" - {additional_info}"

        self.write.write(log_message)
