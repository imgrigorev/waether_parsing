from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import sys


class Parser():
    def __init__(self):
        self.city = None
        self.show_temperature = False
        self.show_humidity = False
        self.show_pressure = False
        self.show_wind_speed = False
        self.weather_link = None
        self.lat = None
        self.lon = None

        for arg in sys.argv:
            if arg.find('--city') >= 0:
                self.city = arg.replace('--city=', '').lower()
            if arg == '--t':
                self.show_temperature = True
            if arg == '--h':
                self.show_humidity = True
            if arg == '--p':
                self.show_pressure = True
            if arg == '--s':
                self.show_wind_speed = True
            if arg == '--all':
                self.show_temperature = True
                self.show_humidity = True
                self.show_pressure = True
                self.show_wind_speed = True


        if not self.city:
            print('Ошибка, город не ввведен')
            return

        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        self.driver = webdriver.Chrome(options=op)
        self.link = f'https://suggest-maps.yandex.ru/suggest-geo?v=8&lang=ru_RU&search_type=weather_v2&n=10&ll=37.6977%2C55.755863&spn=0.5%2C0.5&client_id=weather_v2&svg=1&part={self.city}&pos=3&callback=jQuery78448'
        self.find_lat_and_lon()
        self.parse_weather()

    def find_lat_and_lon(self):
        r = requests.get(self.link)
        soup = bs(r.text, 'html.parser')
        self.lat = soup.text[soup.text.find("lat")+5:soup.text.find(",",soup.text.find("lat"))]
        self.lon = soup.text[soup.text.find("lon") + 5:soup.text.find(",", soup.text.find("lon"))]
        print('Координаты:')
        print('lat', self.lat)
        print('lon', self.lon)

    def parse_weather(self):
        if not self.lat or not self.lon:
            print('Ошибка, координаты города не найдены')
            return

        self.weather_link = f"https://yandex.ru/pogoda/?lat={self.lat}&lon={self.lon}"
        self.driver.get(self.weather_link)
        soup_test = bs(self.driver.page_source, 'html.parser')
        print('Погода в городе: ', self.city)
        if self.show_temperature:
            print("Температура воздуха:", soup_test.find('span', class_='temp__value temp__value_with-unit').text)
        if self.show_humidity:
            print("Влажность:", soup_test.find('div', class_='term term_orient_v fact__humidity')
                  .find('div', class_='term__value').text)
        if self.show_pressure:
            print("Давление:", soup_test.find('div', class_='term term_orient_v fact__pressure')
                  .find('div', class_='term__value').text)
        if self.show_wind_speed:
            print("Скорость ветра:", soup_test.find('span', class_='wind-speed').text, "м.с")


if __name__ == '__main__':
    Parser()