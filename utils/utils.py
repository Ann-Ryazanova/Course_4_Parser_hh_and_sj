def sort_by_salary_min(data):
    """Функция для сортировки зарплаты по минимальной зарплате"""
    data = sorted(data, reverse=False)
    return data


def sort_by_salary_max(data):
    """Функция для сортировки зарплаты по максимальной зарплате"""
    data = sorted(data, key=lambda x: (x.salary_sort_max is not None, x.salary_sort_max), reverse=True)
    return data