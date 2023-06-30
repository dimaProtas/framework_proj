import base64
from protasevich_framework.tempalator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structure_patterns import AppRoute, Debug, weather

site = Engine()
logger = Logger('main')

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    def __call__(self, request):
        logger.log('Главная', '200 OK')
        javascript = {'name': 'JavaScript', 'posted_by': 'Karim Benzema',
                      'text': 'Python - это простой и понятный язык программирования, который подходит для начинающих. Он обладает читаемым синтаксисом и обширной библиотекой, что делает его отличным выбором для изучения основ программирования.'
                              'Язык Python широко используется в различных областях, включая веб-разработку, научные исследования,'
                              'анализ данных и искусственный интеллект. Благодаря своей простоте и гибкости,'
                              'Python позволяет разработчикам быстро прототипировать и создавать эффективные программы,'
                              'что делает его одним из самых популярных языков программирования в мире.',
                      'date': '11 Июня 2023'}
        python = {'name': 'Python', 'posted_by': 'Leo Messi',
                  'text': 'JavaScript - это мощный и универсальный язык программирования, который широко используется веб-разработкой. '
                          'Он позволяет создавать интерактивные и динамические веб-страницы, добавлять функциональность и взаимодействие на стороне клиента.'
                          'Язык JavaScript обладает широкой поддержкой веб-браузерами и может быть использован для создания разнообразных веб-приложений,'
                          'от простых скриптов до сложных одностраничных приложений. Он также имеет большое сообщество разработчиков и обширную экосистему библиотек и фреймворков,'
                          'что делает его идеальным выбором для изучения и применения в сфере веб-разработки.',
                  'date': '13 Июня 2023'}
        c = {'name': 'C#', 'posted_by': 'David Backhem',
             'text': 'C# - это мощный и элегантный язык программирования, разработанный компанией Microsoft.'
                     'Он используется для создания широкого спектра приложений, включая настольные приложения,'
                     'веб-сервисы, игры и мобильные приложения.'
                     'Язык C# обладает простым и понятным синтаксисом, что делает его отличным выбором для начинающих программистов.'
                     'Он предлагает множество возможностей для разработки приложений, включая сильную типизацию,'
                     'объектно-ориентированное программирование, обработку исключений и многопоточность.',
             'date': '16 Июня 2023'}
        return '200 OK', render('index.html', object_list=[javascript, python, c], weather=[weather])


@AppRoute(routes=routes, url='/obout/')
class Obout:
    @Debug('Obout')
    def __call__(self, request):
        logger.log('О нас', '200 OK')
        text = {'text': 'Школа программирования предлагает уникальные образовательные программы, '
                        'разработанные для обучения студентов основам программирования и разработке программного обеспечения, '
                        'чтобы подготовить их к современным технологическим вызовам и открыть возможности '
                        'для карьерного роста в сфере информационных технологий. Школа предлагает структурированные '
                        'учебные планы, квалифицированных преподавателей и доступ к практическим проектам, '
                        'чтобы обеспечить студентам глубокое понимание программирования и навыки, '
                        'необходимые для успешной работы в современной индустрии программного обеспечения.',
                'posted_by': 'Павел Дуров'}
        return '200 OK', render('about.html', object_list=[text], weather=[weather])


@AppRoute(routes=routes, url='/contact/')
class Contact:
    def __call__(self, request):
        logger.log('Контакты', '200 OK')
        contact = {'phone': '+123456789', 'email': 'info@schoolprogramming.com',
                   'address': 'ул. Программистов 123, город, страна', 'website': 'http://www.schoolprogramming.com'}
        return '200 OK', render('contact.html', contact=[contact], weather=[weather])


@AppRoute(routes=routes, url='/programs/')
class Programs:
    def __call__(self, request):
        logger.log('Программы', '200 OK')
        javascript = {'name': 'Основы Django', 'date': 'Сб, 20 февраля 2021', 'time': '11:00 - 14:00'}
        python = {'name': 'Основы Python', 'date': 'Сб, 20 февраля 2021', 'time': '11:00 - 14:00'}
        c = {'name': 'Алгоритмы и структуры данных на Python', 'date': 'Сб, 20 февраля 2021', 'time': '11:00 - 14:00'}
        flask = {'name': 'Основы Flask', 'date': 'Сб, 20 февраля 2021', 'time': '11:00 - 14:00'}
        return '200 OK', render('programs.html', object_list=[python, c, javascript], weather=[weather])


@AppRoute(routes=routes, url='/category/')
class Category:
    @Debug('Category')
    def __call__(self, request):
        logger.log('Категории', '200 OK')
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            logger.log('Категории', 'POST-запрос (созданна новая категория)')
            return '200 OK', render('category.html', object_list=site.categories, weather=[weather])
        else:
            # Отображение списка категорий и формы для создания новой категории
            return '200 OK', render('category.html', object_list=site.categories, create_category=True, weather=[weather])

        # web = {'name': 'Web - разработка'}
        # python = {'name': 'Основы Python'}
        # javascript = {'name': 'основы JavaScript'}
        # c = {'name': 'основы С#'}
        # flask = {'name': 'основы Flask'}
        # flask = {'name': 'Основы Flask'}
        # return '200 OK', render('category.html', object_list=[python, c, javascript, web, flask])


@AppRoute(routes=routes, url='/courses/')
class Courses:
    category_id = -1

    @Debug('courses')
    def __call__(self, request):
        logger.log('Курсы', '200 OK')
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            type_course = data['course_type']
            type_course = site.decode_value(type_course)
            logger.log('Курсы', 'POST-запрос (создан новый курс)')

            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course(type_course, name, category)
                site.courses.append(course)

                with open('template/img/copy.jpg', 'rb') as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')

            return '200 OK', render('courses.html', object_list=category.courses, name=category.name,
                                    id=category.id, image_data=image_data, weather=[weather])

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                with open('template/img/copy.jpg', 'rb') as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')

                return '200 OK', render('courses.html', object_list=category.courses, name=category.name,
                                        id=category.id, image_data=image_data, weather=[weather])
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/copy-course/')
class CopyCourses:
    @Debug('CopyCourses')
    def __call__(self, request):
        request_param = request['request_params']

        try:
            name = request_param['name']
            old_name = site.get_curses(name)
            if old_name:
                new_name = f'{name}_copy'
                new_course = old_name.clone()
                new_course.name = new_name
                site.courses.append(new_course)
                logger.log('Копирование курса', '200 OK (скопирован курс)')

                with open('template/img/copy.jpg', 'rb') as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')

            return '200 OK', render('courses.html', object_list=site.courses,
                                    name=new_course.category.name, image_data=image_data, weather=[weather])
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/users/')
class Users:
    @Debug('Users')
    def __call__(self, request):
        logger.log('Пользователи', '200 OK')
        if request["method"] == 'POST':
            data = request['data']
            name = site.decode_value(data['name'])
            last_name = site.decode_value(data['last_name'])
            email = site.decode_value(data['email'])
            post = site.decode_value(data['post'])
            type_user = site.decode_value(data['type_user'])

            user = site.create_user(type_user, name, last_name, email, post)
            if type_user == 'teacher':
                site.teacher.append(user)
                logger.log('Пользователи', 'POST-запрос (добавлен учитель)')
            elif type_user == 'student':
                site.student.append(user)
                logger.log('Пользователи', 'POST-запрос (добавлен студент)')

        return '200 OK', render('users.html', object_list_teacher=site.teacher, object_list_student=site.student,
                                weather=[weather])
