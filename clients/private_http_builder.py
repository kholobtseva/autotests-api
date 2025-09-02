# from functools import lru_cache
#
# from httpx import Client
# from pydantic import BaseModel, EmailStr, ConfigDict
#
# from clients.authentication.authentication_client import get_authentication_client
# from clients.authentication.authentication_schema import LoginRequestSchema
#
#
# class AuthenticationUserSchema(BaseModel):
#     model_config = ConfigDict(frozen=True)
#
#     email: str
#     password: str
#
#     def __hash__(self):
#         return hash((self.email, self.password))
#
#
# #@lru_cache(maxsize=None)
# def get_private_http_client(user: AuthenticationUserSchema) -> Client:
#     """
#     Функция создаёт экземпляр httpx.Client с аутентификацией пользователя.
#
#     :param user: Объект AuthenticationUserDict с email и паролем пользователя.
#     :return: Готовый к использованию объект httpx.Client с установленным заголовком Authorization.
#     """
#     authentication_client = get_authentication_client()
#
#     login_request = LoginRequestSchema(email=user.email, password=user.password)
#     login_response = authentication_client.login(login_request)
#
#     return Client(
#         timeout=100,
#         base_url='http://localhost:8000',
#         headers={'Authorization': f'Bearer {login_response.token.access_token}'},
#     )

from functools import lru_cache
from httpx import Client
from pydantic import BaseModel, EmailStr, ConfigDict

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema


class AuthenticationUserSchema(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: str
    password: str

    def __hash__(self):
        """Альтернативная реализация хэша"""
        return hash(f"{self.email}:{self.password}")


# Обертка для обхода проблемы с хэшированием
def get_private_http_client(user: AuthenticationUserSchema) -> Client:
    return _get_private_http_client_internal(user.email, user.password)


@lru_cache(maxsize=None)
def _get_private_http_client_internal(email: str, password: str) -> Client:
    authentication_client = get_authentication_client()
    login_request = LoginRequestSchema(email=email, password=password)
    login_response = authentication_client.login(login_request)

    return Client(
        timeout=100,
        base_url='http://localhost:8000',
        headers={'Authorization': f'Bearer {login_response.token.access_token}'},
    )