import time
from faker import Faker

def get_random_email():
    return f"test{time.time()}@example.com" # уникальный email для тестов


from typing import Optional, Literal

fake = Faker("ru_RU")

# Расширенный словарь исключений
GENDER_EXCEPTIONS = {
    # Мужские имена на 'а'/'я'
    'радован': 'male',
    'ника': 'male',
    'савва': 'male',
    'фома': 'male',
    'кузьма': 'male',
    'всеслав': 'male',
    'ярополк': 'male',
    'мирослав': 'male',
    'данила': 'male',

    # Женские имена без стандартных окончаний
    'любовь': 'female',
    'нелли': 'female',
    'ассоль': 'female',
    'николь': 'female'
}


def detect_gender(first_name: str) -> Literal['male', 'female']:
    """Улучшенное определение пола с учетом древнерусских имен"""
    name = first_name.lower().strip()

    # Сначала проверяем явные исключения
    if name in GENDER_EXCEPTIONS:
        return GENDER_EXCEPTIONS[name]

    # Древнерусские и старославянские имена
    if any(name.endswith(end) for end in ('слав', 'мир', 'полк', 'волод', 'рат')):
        return 'male'

    # Стандартные правила
    if name.endswith(('а', 'я', 'ия', 'ина', 'ла', 'на', 'та', 'фа', 'ва', 'ь')):
        return 'female'

    return 'male'


def correct_surname(surname: str, gender: Literal['male', 'female']) -> str:
    """Умная коррекция фамилии с сохранением правильных форм"""
    # Если фамилия уже соответствует полу - не меняем
    if (gender == 'female' and surname.endswith(('ова', 'ева', 'ина', 'ая'))) or \
            (gender == 'male' and not surname.endswith(('ова', 'ева', 'ая'))):
        return surname

    if gender == 'female':
        if surname.endswith(('ов', 'ев', 'ёв', 'ин', 'ын')):
            return surname + 'а'
        elif surname.endswith(('ий', 'ый')):
            return surname[:-2] + 'ая'
        elif surname.endswith('ой'):
            return surname[:-2] + 'ая'
    else:  # male
        if surname.endswith(('ова', 'ева')):
            return surname[:-1]  # Иванова → Иванов
        elif surname.endswith('ая'):
            return surname[:-2] + 'ий'  # Крутая → Крутой

    return surname


def generate_patronymic(first_name: str) -> str:
    """Генерация отчества с проверкой согласованности"""
    gender = detect_gender(first_name)
    if gender == 'female':
        return fake.middle_name_female()
    return fake.middle_name_male()