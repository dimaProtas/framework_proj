from abc import ABC, abstractmethod
from copy import deepcopy
import datetime
from quopri import decodestring
from sqlite3 import connect
from patterns.archi_sys_patterns import DomainObject
from patterns.behavioral_patterns import Subject, ConsoleWrite, FileWrite


Subject = Subject


class User:
    def __init__(self, name, last_name, birthdate, email, password):
        self.name = name
        self.last_name = last_name
        self.birthdate = birthdate
        self.email = email
        self.password = password


class Teacher(User, DomainObject):
    auto_id = 0

    def __init__(self, name, last_name, birthdate, email, password):
        self.id = Teacher.auto_id
        Teacher.auto_id += 1
        super().__init__(name, last_name, birthdate, email, password)



class Student(User, DomainObject):
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


class Interactive(Curses, DomainObject):
    def __init__(self, name, category, type_course=None):
        super().__init__(name, category)
        self.type_course = type_course
        self.category_id = category.id


class Record(Curses, DomainObject):
    def __init__(self, name, category, type_course=None):
        super().__init__(name, category)
        self.type_course = type_course
        self.category_id = category.id


class CourseFactory:
    types = {
        'interactive': Interactive,
        'record': Record,
    }

    @classmethod
    def create(cls, type_, name, category, category_id):
        course = cls.types[type_](name, category, type_course=type_)
        return course

    @classmethod
    def set_course_type(cls, type_, course_type):
        cls.types[type_] = course_type


class Category(DomainObject):
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self, category_mapper):
        course_count = category_mapper.get_course_count_by_category(self.id)
        return course_count


class Engine:
    def __init__(self):
        self.courses = []
        self.categories = []
        self.teacher = []
        self.student = []

    def redact_course(self, id_course, name, category_id, type_course):
        mapper_course = MapperRegistry.get_current_mapper('course')
        course_data = mapper_course.find_by_id(id_course)

        if course_data:
            mapper_category = MapperRegistry.get_current_mapper('category')
            category = mapper_category.find_by_id(category_id)

            if not category:
                raise Exception(f"Категория с ID {category_id} не найдена")

            course_data['name'] = name
            course_data['category'] = category
            course_data['type_course'] = type_course

            mapper_course.update(course_data, category_id)
        else:
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
        maper_category = MapperRegistry.get_current_mapper('category')
        category = maper_category.insert(Category(name, category))
        return category

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
    def create_course(type_, name, category, category_id):
        save = CourseFactory.create(type_, name, category, category_id)
        mapper_course = MapperRegistry.get_current_mapper('course')
        mapper_course.insert(save, category_id)
        return save

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


class UserMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id = item[0]
            name = item[1]
            last_name = item[2]
            birthdate = item[3]
            email = item[4]
            password = item[5]
            student = Student(name, last_name, birthdate, email, password)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT name, last_name, birthdate, email, password FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, last_name, birthdate, email, password) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.last_name, obj.birthdate, obj.email, obj.password))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class TeacherMapper(UserMapper):
    def __init__(self, connection):
        self.cursor = connection.cursor()
        self.tablename = 'teacher'
        super().__init__(connection)


class StudentMapper(UserMapper):
    def __init__(self, connection):
        self.cursor = connection.cursor()
        self.tablename = 'student'
        super().__init__(connection)


class CategoryMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'category'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id = item[0]
            name = item[1]
            category = item[2]
            category = Category(name, category)
            category.id = id
            result.append(category)
        return result

    def find_by_id(self, id):
        statement = f"SELECT name, category FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, category) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.name, obj.category))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET (name, category) VALUES (?, ?) WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.category, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, id):
        try:
            # Получаем все курсы, связанные с удаляемой категорией
            statement_select_courses = f"SELECT id FROM course WHERE category_id={id}"
            self.cursor.execute(statement_select_courses)
            course_ids = [item[0] for item in self.cursor.fetchall()]

            # Удаляем каждый курс
            for course_id in course_ids:
                statement_delete_course = f"DELETE FROM course WHERE id={course_id}"
                self.cursor.execute(statement_delete_course)

            # Удаляем категорию
            statement_delete_category = f"DELETE FROM {self.tablename} WHERE id={id}"
            self.cursor.execute(statement_delete_category)

            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

    def get_course_count_by_category(self, category_id):
        statement = f"SELECT COUNT(*) FROM course WHERE category_id=?"
        self.cursor.execute(statement, (category_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0


class CourseMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'course'

    def all_courses_in_category(self, category_id):
        statement = f"SELECT * FROM course WHERE category_id={category_id}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id = item[0]
            name = item[1]
            type_course = item[2]
            category_id = item[3]
            mapper_category = MapperRegistry.get_current_mapper('category')
            category = mapper_category.find_by_id(category_id)
            course = Curses(name, category)
            course.id = id
            course.type_course = type_course  # Добавляем поле type_course
            result.append(course)
        return result

    def find_course_by_name_and_category(self, name, category_id):
        statement = "SELECT * FROM course WHERE name=? AND category_id=?"
        self.cursor.execute(statement, (name, category_id))
        result = self.cursor.fetchone()
        if result:
            id = result[0]
            name = result[1]
            category_id = result[2]
            # Создайте экземпляр курса и верните его, или верните только нужные данные
            # в зависимости от ваших потребностей
            return Curses(id, name, category_id)
        else:
            return None

    def find_by_id(self, id):
        statement = f"SELECT id, name, type_course, category_id FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            id, name, type_course, category_id = result
            return {'id': id, 'name': name, 'type_course': type_course, 'category_id': category_id}
        else:
            raise RecordNotFoundException(f"Course with id={id} not found")

    def insert(self, obj, category_id):
        statement = f"INSERT INTO {self.tablename} (name, type_course, category_id) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.type_course, category_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj, category_id):
        statement = f"UPDATE {self.tablename} SET name=?, category_id=? WHERE id=?"

        if 'name' in obj:
            self.cursor.execute(statement, (obj['name'], category_id, obj['id']))
        else:
            raise Exception(f"Не удалось обновить запись. Отсутствует атрибут 'name' в переданном объекте.")

        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, id):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('db.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        'teacher': TeacherMapper,
        'category': CategoryMapper,
        'course': CourseMapper,
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Student):
            return StudentMapper(connection)
        elif isinstance(obj, Teacher):
            return TeacherMapper(connection)
        elif isinstance(obj, Category):
            return CategoryMapper(connection)
        elif isinstance(obj, Curses):
            return CourseMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
