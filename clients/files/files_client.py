from httpx import Response
from pathlib import Path
from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from .files_schema import (
    FileSchema,
    CreateFileRequestSchema,
    CreateFileResponseSchema,
    GetFileResponseSchema
)


class FilesClient(APIClient):
    """
    Клиент для работы с /api/v1/files
    """

    def get_file_api(self, file_id: str) -> Response:
        """
        Метод получения файла по идентификатору.

        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"/api/v1/files/{file_id}")

    def create_file_api(self, request: CreateFileRequestSchema) -> Response:
        """
        Метод создания файла.

        :param request: Данные для создания файла.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        if not Path(request.upload_file).exists():
            raise FileNotFoundError(f"Файл {request.upload_file} не найден")

        return self.post(
            "/api/v1/files",
            data={
                "filename": request.filename,
                "directory": request.directory
            },
            files={"upload_file": open(request.upload_file, 'rb')}
        )

    def delete_file_api(self, file_id: str) -> Response:
        """
        Метод удаления файла.

        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"/api/v1/files/{file_id}")

    def get_file(self, file_id: str) -> GetFileResponseSchema:
        """
        Метод получения файла с валидацией ответа.

        :param file_id: Идентификатор файла.
        :return: Валидированные данные файла.
        """
        response = self.get_file_api(file_id)
        return GetFileResponseSchema.model_validate_json(response.text)

    def create_file(self, request: CreateFileRequestSchema) -> CreateFileResponseSchema:
        """
        Метод создания файла с валидацией ответа.

        :param request: Данные для создания файла.
        :return: Валидированные данные созданного файла.
        """
        response = self.create_file_api(request)
        return CreateFileResponseSchema.model_validate_json(response.text)


def get_files_client(user: AuthenticationUserSchema) -> FilesClient:
    """
    Функция создаёт экземпляр FilesClient с уже настроенным HTTP-клиентом.

    :param user: Данные аутентификации пользователя.
    :return: Готовый к использованию FilesClient.
    """
    return FilesClient(client=get_private_http_client(user))