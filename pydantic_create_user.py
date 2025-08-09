from pydantic import BaseModel, EmailStr, Field, constr
import httpx
from tools.fakers import fake, generate_patronymic, correct_surname, detect_gender
from faker import Faker

fake = Faker("ru_RU")

class UserSchema(BaseModel):
    """
    Pydantic модель для представления данных пользователя.

    Attributes:
        id: Уникальный идентификатор пользователя
        email: Email пользователя (валидируется на корректность)
        last_name: Фамилия пользователя (алиас lastName)
        first_name: Имя пользователя (алиас firstName)
        middle_name: Отчество пользователя (алиас middleName)
    """
    id: str
    email: EmailStr
    last_name: str= Field(alias="lastName")
    first_name: str= Field(alias="firstName")
    middle_name: str= Field(alias="middleName")

    def get_username(self) -> str:
        """
        Генерирует отображаемое имя пользователя в формате 'Имя Фамилия'.

        Returns:
            Строка с полным именем пользователя
        """
        return f"{self.first_name} {self.middle_name} {self.last_name}"

class CreateUserRequestSchema(BaseModel):
    """
        Pydantic модель для запроса создания пользователя.

        Attributes:
            email: Email пользователя (1-250 символов)
            password: Пароль пользователя (1-250 символов)
            last_name: Фамилия пользователя (1-50 символов, алиас lastName)
            first_name: Имя пользователя (1-50 символов, алиас firstName)
            middle_name: Отчество пользователя (1-50 символов, необязательное, алиас middleName)
    """
    email: EmailStr = Field(
        ...,  # Обязательное поле
        examples=["user@example.com"],
        description="Email (1-250 символов)",
        min_length=1,
        max_length=250
    )
    password: constr(min_length=1, max_length=250) = Field(...,
        examples=["securepassword123"],
        description="User's password (1-250 characters)")
    last_name: str= Field(
        ...,
        alias="lastName",
        examples=["Иванов"],
        description="Фамилия (1-50 символов)",
        min_length=1,
        max_length=50
    )
    first_name: str= Field(
        ...,
        alias="firstName",
        examples=["Петр"],
        description="Имя (1-50 символов)",
        min_length=1,
        max_length=50)
    middle_name: str= Field(
        None,
        alias="middleName",
        examples=["Сергеевич"],
        description="Отчество (1-50 символов, необязательно)",
        min_length=1,
        max_length=50
    )

class CreateUserResponseSchema(BaseModel):
    """
    Pydantic модель для ответа после создания пользователя.

    Attributes:
    user: Объект созданного пользователя (UserSchema)
    """
    user: UserSchema


# Создание тестового пользователя
user = UserSchema(
    id="user-id",
    email=fake.email(),
    lastName=fake.last_name(),
    firstName= fake.first_name(),
    middleName=fake.middle_name()
)


# Подготовка payload для запроса
payload = CreateUserRequestSchema(
    email= user.email,
    password= 'string',
    lastName= user.last_name,
    firstName= user.first_name,
    middleName= user.middle_name
)

gender = detect_gender(user.first_name)
payload.middle_name = generate_patronymic(payload.first_name)
payload.last_name = correct_surname(user.last_name, gender)

print("Отправляемые данные:", payload.model_dump(by_alias=True))

# Отправка HTTP-запроса
try:
    response = httpx.post("http://localhost:8000/api/v1/users",
                          json = payload.model_dump(by_alias=True),
                          headers={"Content-Type": "application/json"})
    print("Статус код:", response.status_code)
    print("Ответ сервера:", response.json())
except httpx.HTTPError as e:
    print(f"Ошибка при выполнении запроса: {e}")






