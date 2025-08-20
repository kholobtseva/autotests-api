import pytest
from http import HTTPStatus
from tools.assertions.base import assert_status_code
from tools.assertions.users import assert_get_user_response
from tools.assertions.schema import validate_json_schema
from clients.users.users_schema import GetUserResponseSchema


@pytest.mark.regression
@pytest.mark.users
def test_get_user_me(function_user, private_users_client):
    # Выполняем запрос
    response = private_users_client.get_user_me_api()

    # Проверяем статус-код
    assert_status_code(response.status_code, HTTPStatus.OK)

    # Преобразуем JSON-ответ
    get_user_response = GetUserResponseSchema.model_validate_json(response.text)

    # Сравниваем с данными созданного пользователя
    assert_get_user_response(get_user_response, function_user.response)

    # Валидируем JSON-схему ответа
    validate_json_schema(response.json(), GetUserResponseSchema.model_json_schema())
