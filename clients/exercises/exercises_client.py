from httpx import Response, QueryParams

from clients.api_client import APIClient
from clients.exercises.exercises_schema import (
    GetExercisesQuerySchema,
    CreateExerciseRequestSchema,
    UpdateExerciseRequestSchema,
    GetExercisesResponseSchema,
    ExerciseSchema,
    CreateExerciseResponseSchema,
    UpdateExerciseResponseSchema,
)
from clients.private_http_builder import (
    AuthenticationUserSchema,
    get_private_http_client,
)


class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises
    """

    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """
        Метод получения списка упражнений.

        :param query: Словарь с courseId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """

        params = QueryParams(*query)
        return self.get(f'/api/v1/exercises', params=params)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод получения упражнения.

        :param exercise_id: Идентификатор упражнения.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f'/api/v1/exercises/{exercise_id}')

    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """
        Метод создания упражнения.

        :param request: Словарь с title, courseId, maxScore, minScore,
        orderIndex, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post('/api/v1/exercises', json=request.model_dump(by_alias=True))

    def update_exercise_api(
        self, exercise_id: str, request: UpdateExerciseRequestSchema
    ) -> Response:
        """
        Метод обновления упражнения.

        :param exercise_id: Идентификатор упражнения.
        :param request: Словарь с title, maxScore, minScore,
        orderIndex, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(
            f'/api/v1/exercises/{exercise_id}', json=request.model_dump(by_alias=True)
        )

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод удаления упражнения.

        :param exercise_id: Идентификатор упражнения.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f'/api/v1/exercises/{exercise_id}')

    def get_exercises(
        self, query: GetExercisesQuerySchema
    ) -> GetExercisesResponseSchema:
        response = self.get_exercises_api(query).text
        return GetExercisesResponseSchema.model_validate_json(response)

    def get_exercise(self, exercise_id: str) -> ExerciseSchema:
        response = self.get_exercise_api(exercise_id).text
        return ExerciseSchema.model_validate_json(response)

    def create_exercise(
        self, request: CreateExerciseRequestSchema
    ) -> CreateExerciseResponseSchema:
        response = self.create_exercise_api(request).text
        return CreateExerciseResponseSchema.model_validate_json(response)

    def update_exercise(
        self, exercise_id: str, request: UpdateExerciseRequestSchema
    ) -> UpdateExerciseResponseSchema:
        response = self.update_exercise_api(exercise_id, request).text
        return UpdateExerciseResponseSchema.model_validate_json(response)


def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию объект ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))