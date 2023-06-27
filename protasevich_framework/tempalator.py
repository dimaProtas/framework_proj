from jinja2 import Environment, FileSystemLoader


def render(template_name, folder='template', **kwargs):
    file_loader = FileSystemLoader(folder)
    env = Environment(loader=file_loader)

    template = env.get_template(template_name)
    return template.render(**kwargs)


#тест шаблонизатора
if __name__ == '__main__':
    output_test = render('courses.html', object_list=[{'name': 'Valera'}, {'name': 'Roma'}])
    print(output_test)
