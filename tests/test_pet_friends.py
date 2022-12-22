from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_withot_photo(name='Барбоскин', animal_type='двортерьер',
                                     age='4'):
    """Проверяем что можно добавить питомца без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_post_add_petphoto(pet_photo='images/P1040103.jpg'):
    """Добавление фото к созданному питомцу без фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']  # id изменяемого питомца (первый в списке)
    value_image1 = my_pets['pets'][0]['pet_photo']  # получаем код image изменяемой фотки
    print(f"\nvalue_image1: {len(str(value_image1))} символов: {value_image1}", sep='')

    # Добавляем фото
    status, result = pf.post_add_pet_photo (auth_key, pet_photo, pet_id)

    # Получаем значение картинки1:
    value_image1 = result.get('pet_photo')
    print('\n', f"value_image1: {len(value_image1)} символов: {value_image1}", sep='')

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # Если полученное значение ключа одной картинки не равно значению ключа другой картинки - PASSED:


def test_changes_petphoto(pet_photo='images/153119778814935570.jpg'):
    """Тестируем: Изменение фото первого питомца в списке"""


    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']  # id изменяемого питомца (первый в списке)
    value_image1 = my_pets['pets'][0]['pet_photo']  # получаем код image изменяемой фотки
    print(f"\nvalue_image1: {len(str(value_image1))} символов: {value_image1}", sep='')

    # Добавляем фото
    status, result = pf.change_pet_photo(auth_key, pet_photo, pet_id)
    value_image2 = result.get('pet_photo')  # получаем код image новой фотки
    print(f"value_image2: {len(str(value_image2))} символов: {value_image2}")

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # Если полученное значение кода одной картинки не равно значению кода другой картинки - PASSED:
    assert value_image1 != value_image2

def test_add_new_pet_with_valid_data(name='Кисяо', animal_type='котэ',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_data (name='Кисяо', animal_type='/*!@',
                                     age='четыре', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с не корректными данными"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    if len(my_pets['pets']) > 0:
        assert status == 200
        assert result['animal_type'] == animal_type
        assert result['age'] == age
    else:
        raise Exception("There is no my pets")


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиcок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_all_pets():
    """Тестируем возможность удаления всех питомцев пользователя"""
    # Для запуска нужно в т.ч. добавить запрос на удаление питомца: delete_pet
    # Получаем ключ auth_key и запрашиваем список питомцев пользователя:
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    # Получаем в цикле id всех питомцев из списка и отправляем запрос на удаление:
    for id_pet in my_pets["pets"]:
        pf.delete_pet(auth_key, id_pet["id"])
    # Ещё раз запрашиваем список питомцев:
    status, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


