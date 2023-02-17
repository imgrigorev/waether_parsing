from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs

class Parser():
    def __init__(self):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        self.driver = webdriver.Chrome(options=op)
        self.city_name = input("Введите город: ")
        print("Идет поиск, пожалуйста, подождитеы")
        self.get_weather()
        self.print_results(input('Показать темературу y/n? '),input('Показать влажность y/n? '),
                           input('Показать давление y/n? '),input('Показать скорость ветра y/n? '))

    def get_weather(self):
        self.driver.get("https://yandex.ru/pogoda/")
        element = self.driver.find_element(By.TAG_NAME, "input")
        element.send_keys(f"{self.city_name}")
        time.sleep(2)
        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)
        self.soup = bs(self.driver.page_source, 'html.parser')
        self.driver.quit()

    def print_results(self,temp,wet,bar,wind):
        if temp == 'y':
            print("Температура воздуха:",self.soup.find('span', class_='temp__value temp__value_with-unit').text)
        if wet == 'y':
            print("Влажность:",self.soup.find('div', class_='term term_orient_v fact__humidity').find('div', class_='term__value').text)
        if bar == 'y':
            print("Давление:",self.soup.find('div', class_='term term_orient_v fact__pressure').find('div', class_='term__value').text)
        if wind == 'y':
            print("Скорость ветра:",self.soup.find('span', class_='wind-speed').text,"м.с")





if __name__ == '__main__':
    Parser()
