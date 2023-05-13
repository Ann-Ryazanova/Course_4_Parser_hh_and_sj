from abc import ABC, abstractmethod
import json
import requests
import os


class Engine(ABC):
    """
    Абстрактный метод от, которого наследуются HeadHunterAPI() и SuperJobAPI()
    """

    @abstractmethod
    def get_request(self):
        pass


class HeadHunterAPI(Engine):
    """Класс для работы с API сайтом hh.ru"""

    def __init__(self, keyword: str):
        self.__header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/110.0.0.0 YaBrowser/23.3.3.721 Yowser/2.5 Safari/537.36"
        }
        self.__params = {"text": keyword, "page": 0, "per_page": 100}
        self.__vacancies = []

    @property
    def vacancies(self):
        return self.__vacancies

    def get_request(self):
        """
        Функция для запроса данных через API с HeadHunter.
        """
        response = requests.get("https://api.hh.ru/vacancies",
                                params=self.__params,
                                headers=self.__header)

        if response.status_code != 200:
            raise f"Request failed with status code: {response.status_code}"
        return response.json()['items']

    def get_vacancies(self, pages_count: int):
        """Функция позволяющий положить данные о вакансиях в список"""

        while self.__params['page'] < pages_count:
            print(f"Идет поиск на HeadHunter. Страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except Exception as err:
                print(f"Произошла ошибка при получении вакансий: {err}.")
                break

            print(f"Найдено {len(values)} вакансий")
            self.__params['page'] += 1
            self.__vacancies.extend(values)

        return self.__vacancies

    def info_vacancy(self):
        """Функция для форматирования данных для работы с class Connector"""

        info_vacancies = []

        for vacancy in self.__vacancies:
            if vacancy['salary']:
                salary_min, salary_max, currency = vacancy['salary']['from'], vacancy['salary']['to'], \
                    vacancy['salary']['currency']
                info_vacancies.append({
                    "id_vacancy": vacancy['id'],
                    "title": vacancy['name'],
                    "salary_min": salary_min,
                    "salary_max": salary_max,
                    "currency": currency,
                    "employer": vacancy['employer']['name'],
                    "url": vacancy['alternate_url'],
                    "address": vacancy['area']['name']
                })

        return info_vacancies


class SuperJobAPI(Engine):
    """ Класс для работы с API сайтом SuperJob """

    def __init__(self, keyword: str):
        self.__header = {"X-Api-App-Id": os.getenv('SJ_API_KEY')}
        self.__params = {"keyword": keyword, "page": 0, "per_page": 100}
        self.__vacancies = []

    @property
    def vacancies(self):
        return self.__vacancies

    def get_request(self):
        """ Функция для запроса данных через API с HeadHunter."""

        response = requests.get("https://api.superjob.ru/2.0/vacancies/", params=self.__params, headers=self.__header)

        if response.status_code != 200:
            raise f"Request failed with status code: {response.status_code}"

        return response.json()['objects']

    def get_vacancies(self, pages_count=1):
        """Функция позволяющий положить данные о вакансиях в список"""

        while self.__params['page'] < pages_count:
            print(f"Идет поиск на SuperJob. Страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except Exception as err:
                print(f"Произошла ошибка при получении вакансий: {err}")
                break

            print(f"Найдено {len(values)} вакансий")
            self.__params['page'] += 1
            self.__vacancies.extend(values)

        return self.__vacancies

    def info_vacancy(self):
        """Функция для форматирования данных для работы с class Connector"""

        info_vacancies = []

        for vacancy in self.__vacancies:
            salary_min = vacancy['payment_from']
            salary_max = vacancy['payment_to']
            currency = vacancy['currency']

            info_vacancies.append({
                "id_vacancy": vacancy['id'],
                "title": vacancy['profession'],
                "salary_min": salary_min,
                "salary_max": salary_max,
                "currency": currency,
                "employer": vacancy['firm_name'],
                "url": vacancy['link'],
                "address": vacancy['address']
            })

        return info_vacancies


class Connector:
    """Класс для создания и записи файла, полученного по API"""

    def __init__(self, keyword: str):
        self.__filename = f"{keyword.title()}.json"

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, data: list):
        """Функция для записи вакансий в файл"""
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

    def select(self):
        """Функция для чтения файла и создания списка экземпляров класса Vacancy"""
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        vacancies = []

        for row in data:
            vacancies.append(Vacancy(row['id_vacancy'], row['title'], row['salary_min'], row['salary_max'],
                                     row['currency'], row['employer'], row['url'], row['address']))

        return vacancies


class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, id_vacancy: str, title: str, salary_min: int | None, salary_max: int | None, currency: str,
                 employer: str, url: str, address: str):

        self.id_vacancy = id_vacancy
        self.title = title
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.employer = employer
        self.url = url
        self.address = address

        """Введение значений: salary_sort_min и salary_sort_max для сортировки по минимальной и максимальной зарплате.
        Значения переводятся в rub в соответствие с курсом валюты"""

        self.salary_sort_min = salary_min
        self.salary_sort_max = salary_max

        if currency and currency == 'USD':
            self.salary_sort_min = self.salary_sort_min * 77 if self.salary_sort_min else None
            self.salary_sort_max = self.salary_sort_max * 77 if self.salary_sort_max else None

        elif currency and currency == 'UZS':
            self.salary_sort_min = self.salary_sort_min * 67 if self.salary_sort_min else None
            self.salary_sort_max = self.salary_sort_max * 67 if self.salary_sort_max else None

        elif currency and currency == 'KZT':
            self.salary_sort_min = self.salary_sort_min * 17 if self.salary_sort_min else None
            self.salary_sort_max = self.salary_sort_max * 17 if self.salary_sort_max else None

        elif currency and currency == 'EUR':
            self.salary_sort_min = self.salary_sort_min * 84 if self.salary_sort_min else None
            self.salary_sort_max = self.salary_sort_max * 84 if self.salary_sort_max else None

    def __str__(self):
        """Функция для вывода данных для пользователя"""
        salary_min = f"от {self.salary_min}" if self.salary_min else ""
        salary_max = f"до {self.salary_max}" if self.salary_max else ""
        currency = f"{self.currency}" if self.currency else ""

        if self.salary_min == 0 or None and self.salary_max == 0 or None:
            salary_min = "Не указана"

        if self.address is None:
            self.address = "Не указан"

        return f"Вакансия: {self.title}\n" \
               f"Зарплата: {salary_min} {salary_max} {currency}\n" \
               f"Город: {self.address}\n" \
               f"Работадатель: {self.employer}\n" \
               f"URL: {self.url}"

    def __gt__(self, other):
        """Метод за счет, которого осуществляется сравнение"""
        if not other.salary_sort_min:
            return True
        if not self.salary_sort_min:
            return False
        return self.salary_sort_min >= other.salary_sort_min
