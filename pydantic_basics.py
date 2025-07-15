"""{
  "course": {
    "id": "string",
    "title": "string",
    "maxScore": 0,
    "minScore": 0,
    "description": "string",
    "previewFile": {
      "id": "string",
      "filename": "string",
      "directory": "string",
      "url": "https://example.com/"
    },
    "estimatedTime": "string",
    "createdByUser": {
      "id": "string",
      "email": "user@example.com",
      "lastName": "string",
      "firstName": "string",
      "middleName": "string"
    }
  }
}"""

from pydantic import BaseModel, Field, ConfigDict, computed_field, HttpUrl, EmailStr, ValidationError
from pydantic.alias_generators import to_camel
import uuid

class FileSchema(BaseModel):
    id: str
    filename: str
    directory: str
    url: HttpUrl

class UserSchema(BaseModel):
    id: str
    email: EmailStr
    last_name: str= Field(alias="lastName")
    first_name: str= Field(alias="firstName")
    middle_name: str= Field(alias="middleName")

    @computed_field()
    def username(self) ->str:
        return f"{self.first_name} {self.last_name}"


    def get_username(self) -> str:
        return f"{self.first_name} {self.last_name}"


class CourseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str = Field(default_factory= lambda: str(uuid.uuid4()))
    title: str = "Python API course"
    #max_score: int
    max_score: int = Field(alias= "maxScore", default=1000)
    #min_score: int
    min_score: int = Field(alias= "minScore", default=100)
    description: str = "Python API"
    preview_file: FileSchema= Field(alias="previewFile")
    #estimated_time: str
    estimated_time: str = Field(alias= "estimatedTime", default="2 week")
    created_by_user: UserSchema = Field(alias="createdByUser")

course_default_model = CourseSchema(
    id= "course-id",
    title= "Python API course",
    maxScore= 100,
    minScore= 10,
    description= "Python API",
    estimatedTime= "1 week",
    previewFile= FileSchema(
        id="file-id",
        filename= "file.png",
        url="http://localhost:8000",
        directory= "courses"
    )
    ,
    createdByUser= UserSchema(
        id= "user-id",
        email= "user@gmail.com",
        lastName= "Bond",
        firstName= "Zara",
        middleName= "Alice"
    )
)

course_dict = {
    "id": "course-id",
    "title": "Python API course",
    "maxScore": 100,
    "minScore": 10,
    "description": "Python API",
    "estimatedTime": "1 week",
    "previewFile": {
        "id": "file-id",
        "filename": "file.png",
        "url": "http://localhost:8000",
        "directory": "courses"
    },
    "createdByUser": {
        "id": "user-id",
        "email": "user@gmail.com",
        "lastName": "Bond",
        "firstName": "Zara",
        "middleName": "Alice"
    }

}

course_dict_module = CourseSchema(**course_dict)

print("Course default model: ", course_default_model)
print("Course default model: ", course_default_model.estimated_time)

print("Course dict module: ", course_dict_module)

course_json = """ {
    "id": "course-id",
    "title": "Python API course",
    "maxScore": 100,
    "minScore": 10,
    "description": "Python API",
    "estimatedTime": "1 week",
    "previewFile": {
        "id": "file-id",
        "filename": "file.png",
        "url": "http://localhost:8000",
        "directory": "courses"
    },
    "createdByUser": {
        "id": "user-id",
        "email": "user@gmail.com",
        "lastName": "Bond",
        "firstName": "Zara",
        "middleName": "Alice"
    }

} """

course_json_module = CourseSchema.model_validate_json(course_json)
print("Course json model: ", course_json_module)

print(course_json_module.model_dump(by_alias=True))
print(course_json_module.model_dump_json(by_alias=True))

user = UserSchema(
        id= "user-id",
        email= "user@gmail.com",
        lastName= "Bond",
        firstName= "Zara",
        middleName= "Alice"
)

print(user.get_username(), user.username)

file = FileSchema(
        id="file-id",
        filename= "file.png",
        url="http://localhost:8000",
        directory= "courses"
)

try:
    file = FileSchema(
        id="file-id",
        filename="file.png",
        url="localhost",
        directory="courses"
    )
except ValidationError as error:
    print(error)
    print(error.errors())

print(file)