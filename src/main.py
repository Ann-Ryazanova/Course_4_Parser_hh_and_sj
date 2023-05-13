from classes.classes import HeadHunterAPI, Connector, SuperJobAPI
from utils.utils import sort_by_salary_min, sort_by_salary_max


def main():
    """Функция для работы с пользователем. Позволяет выбрать площадку для поиска вакансий"""

    print("Приветствуем Вас! Данная программа предназначена для поиска вакансий на HeadHunter и SuperJob.\n")

    choice_platform = input('Пожалуйста, выберете один из доступных сервисов по его номеру:\n'
                            '1: SuperJob\n'
                            '2: HeadHunter\n').strip()

    while choice_platform not in ('1', '2'):
        choice_platform = input('Платформа не обнаружена, пожалуйста, повторите ввод: ').strip()

    if choice_platform == '1':

        formatted_vacancies = []

        print('Вы выбрали SuperJob для поиска необходимых вакансий.')
        key_word = input("Введите название вакансии или ключевое слово для поиска\n")
        pages_count = int(input("Введите количество страниц для поиска\n"))

        sj_api = SuperJobAPI(key_word)
        sj_api.get_vacancies(pages_count)
        formatted_vacancies.extend(sj_api.info_vacancy())
        json_sever = Connector(key_word)
        json_sever.add_vacancies(formatted_vacancies)
        vacancies = json_sever.select()

        while True:
            command = input('Пожалуйста, выберете один из пунктов и введите его номер:\n'
                            '1: Вывести список вакансий;\n'
                            '2: Вывести список вакансий (отсортированный по минимальной зарплате);\n'
                            '3: Вывести список вакансий (отсортированный по максимальной зарплате) ; \n'
                            '4: Выход\n').strip()

            if command.lower() == "1":
                vacancies = vacancies

            elif command.lower() == "2":
                vacancies = sort_by_salary_min(vacancies)

            elif command.lower() == "3":
                vacancies = sort_by_salary_max(vacancies)

            elif command.lower() == "4":
                print("Спасибо, что воспользовались нашей программой.\n"
                      "До свидания!")
                break

            for vacancy in vacancies:
                print(vacancy, end=f"\n\n{'_' * 100}\n\n")

    elif choice_platform == '2':

        formatted_vacancies = []

        print('Вы выбрали HeadHunter для поиска необходимых вакансий.')
        key_word = input("Введите название вакансии или ключевое слово для поиска\n")
        pages_count = int(input("Введите количество страниц для поиска\n"))

        hh_api = HeadHunterAPI(key_word)
        hh_api.get_vacancies(pages_count)
        formatted_vacancies.extend(hh_api.info_vacancy())
        json_sever = Connector(key_word)
        json_sever.add_vacancies(formatted_vacancies)
        vacancies = json_sever.select()

        while True:
            command = input('Пожалуйста, выберете один из пунктов и введите его номер:\n'
                            '1: Вывести список вакансий;\n'
                            '2: Вывести список вакансий (отсортированный по минимальной зарплате);\n'
                            '3: Вывести список вакансий (отсортированный по максимальной зарплате) ; \n'
                            '4: Выход\n').strip()

            if command.lower() == "1":
                vacancies = vacancies

            elif command.lower() == "2":
                vacancies = sort_by_salary_min(vacancies)

            elif command.lower() == "3":
                vacancies = sort_by_salary_max(vacancies)

            elif command.lower() == "4":
                print("Спасибо, что воспользовались нашей программой.\n"
                      "До свидания!")
                break

            for vacancy in vacancies:
                print(vacancy, end=f"\n\n{'_' * 180}\n\n")


if __name__ == '__main__':
    main()
