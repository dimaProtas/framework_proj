import time
import abc
import re
import requests
import threading
from bs4 import BeautifulSoup


# структурный паттерн Декоратор
class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


# структурный паттерн Декоратор
class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            t = time.time()
            result = func(*args, **kwargs)
            te = time.time()
            print(f'{self.name} time{te - t}')
            return result

        return wrapper


class WeatherService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_weather(self):
        pass


class WeatherCurrencyService(WeatherService):
    def get_weather(self):
        url = 'https://yandex.ru/pogoda/'
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        weather_element = soup.find('div', class_='title-icon__text')

        if weather_element is not None:
            weather_text = weather_element.get_text(strip=True)
        else:
            weather_text = 'Не удалось получить информацию о погоде'

        # Обрезание описания погоды до точки
        dot_index = weather_text.find('·')
        if dot_index != -1:
            weather_info = weather_text[:dot_index]
        else:
            weather_info = 'Не удалось получить информацию о погоде'

        # Извлечение температуры с помощью регулярного выражения
        temperature_range_match = re.search(r'(\+\d+⁠…⁠\+\d+⁠°)', weather_text)
        if temperature_range_match:
            temperature_range = temperature_range_match.group()
        else:
            temperature_range = 'Не удалось получить информацию о температуре'

        # Извлечение скорости ветра
        wind_speed = 'Не удалось получить информацию о ветре'
        dots = weather_text.split('·')
        if len(dots) >= 3:
            wind_speed = '·'.join(dots[2:]).strip()

        weather = {'temperature_range': temperature_range, 'weather_info': weather_info, 'wind_speed': wind_speed}

        return weather


# патерн Заместитель(Proxy)
class ProxyWeatherService(WeatherCurrencyService):
    def __init__(self):
        self.currencyWeatherService = WeatherCurrencyService()
        self.rate = dict()
        self.start_timer()

    def start_timer(self):
        self.timer = threading.Timer(3 * 60 * 60, self.clear_rate)  # Запуск таймера каждые 3 часа
        self.timer.start()

    def clear_rate(self):
        self.rate = {}  # Очистка словаря
        self.start_timer()  # Запуск таймера для следующей очистки

    def get_weather(self):
        if not self.rate:
            weather = self.currencyWeatherService.get_weather()
            self.rate.update(weather)
        return self.rate


weather_data = ProxyWeatherService()
weather = weather_data.get_weather()
print(weather)