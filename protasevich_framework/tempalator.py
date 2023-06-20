from jinja2 import Template
from os.path import join


def render(template_name, folder='template', **kwargs):

    file_path = join(folder, template_name)

    with open(file_path, encoding='utf-8') as f:

        template = Template(f.read())

    return template.render(**kwargs)


#тест шаблонизатора
if __name__ == '__main__':
    output_test = render('authors.html', object_list=[{'name': 'Valera'}, {'name': 'Roma'}])
    print(output_test)
