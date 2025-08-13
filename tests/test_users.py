import http

from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from http import HTTPStatus

from tools.assertions.schema import validate_json_schema


def test_create_user():
    public_users_client = get_public_users_client()

    request = CreateUserRequestSchema()
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    assert response.status_code == http.HTTPStatus.OK, "Некорректный статус-код ответа"
    assert response_data.user.email == request.email, "Некорректный email пользователя"
    assert response_data.user.last_name == request.last_name, "Некорректная фамилия пользователя"
    assert response_data.user.first_name == request.first_name, "Некорректное имя пользователя"
    assert response_data.user.middle_name == request.middle_name, "Некорректное отчество пользователя"

    validate_json_schema(response.json(), response_data.model_json_schema())