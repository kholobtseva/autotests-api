from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ExerciseSchema(BaseModel):
    """
    Описание структуры упражнения.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore", default=0)
    min_score: int = Field(alias="minScore", default=0)
    order_index: int = Field(alias="orderIndex", default=0)
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class CreateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание упражнения.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore", default=0)
    min_score: int = Field(alias="minScore", default=0)
    order_index: int = Field(alias="orderIndex", default=0)
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class CreateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания упражнения.
    """
    exercise: ExerciseSchema


class UpdateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление упражнения.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: Optional[str] = None
    max_score: Optional[int] = Field(alias="maxScore", default=0)
    min_score: Optional[int] = Field(alias="minScore", default=0)
    order_index: Optional[int] = Field(alias="orderIndex", default=0)
    description: Optional[str] = None
    estimated_time: Optional[str] = Field(alias="estimatedTime", default=None)


class GetExercisesResponseSchema(BaseModel):
    """
    Описание структуры ответа получения списка упражнений.
    """
    exercises: list[ExerciseSchema]


class GetExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа получения упражнения.
    """
    exercise: ExerciseSchema