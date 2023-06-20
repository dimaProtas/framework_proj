from urllib.parse import unquote, parse_qs
from quopri import decodestring


def parse_input_data(data: str):
    result = {}
    if data:
        params = data.split('&')
        for item in params:
            k, v = item.split('=')
            result[k] = v
    return result


def process_get_data(environ):
    query_string = environ.get('QUERY_STRING', '')
    # query_data = parse_qs(query_string) # parse_qs так же можно использовать для парсинга post и get запросов
    query_data = parse_input_data(query_string)
    decoded_data = decode_value(query_data)
    # with open('data_get.txt', 'a') as f:
    #     if f.tell() == 0:
    #         f.write('Полученные Get запросы:\n'
    #                 '-----------------------------------------\n')
    #     f.write(str(query_data) + '\n')
    print('Received GET data:', decoded_data)


def process_form_data(environ):
    content_length = int(environ.get('CONTENT_LENGTH', 0))
    form_data = environ['wsgi.input'].read(content_length).decode('utf-8')
    # decode_form_data = unquote(form_data) #использовал unquoдte для декодировки латиницы(декодирует с + вместо пробела)
    request_data = parse_input_data(form_data)
    result = decode_value(request_data)
    with open('data_post.txt', 'a') as f:
        if f.tell() == 0:
            f.write('Имя                Email            Сообщение\n'
                    '------------------------------------------------\n')
        f.write(f'{result["name"]}\t{result["email"]}\t{result["message"]}  \n')
    # Разбор данных из формы и вывод в терминал
    print('Received form data:', result)


def decode_value(data):
    new_data = {}
    for k, v in data.items():
        val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
        key = bytes(k.replace('%', '=').replace("+", " "), 'UTF-8')
        key_decode_str = decodestring(key).decode('UTF-8')
        val_decode_str = decodestring(val).decode('UTF-8')
        new_data[key_decode_str] = val_decode_str
    return new_data
