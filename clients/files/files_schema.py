from pydantic import BaseModel, Field, ConfigDict


class FileSchema(BaseModel):
    """
    Описание структуры файла.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    filename: str
    directory: str
    url: str


class CreateFileRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание файла.
    """
    model_config = ConfigDict(populate_by_name=True)

    filename: str
    directory: str
    upload_file: str = Field(alias="uploadFile")


class CreateFileResponseSchema(BaseModel):
    """
    Описание структуры ответа создания файла.
    """
    file: FileSchema


class GetFileResponseSchema(BaseModel):
    """
    Описание структуры ответа получения файла.
    """
    file: FileSchema