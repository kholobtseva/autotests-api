from clients.private_http_builder import AuthenticationUserDict
from clients.users.private_users_client import get_private_users_client
from clients.users.public_users_client import get_public_users_client, CreateUserRequestDict
from tools.fakers import get_random_email

# Инициализируем клиент PublicUsersClient
public_users_client = get_public_users_client()

# Инициализируем запрос на создание пользователя
create_user_request = CreateUserRequestDict(
    email= get_random_email(),
    password= "string",
    lastName= "string",
    firstName= "string",
    middleName= "string"
)

# Отправляем POST запрос на создание пользователя
create_users_response = public_users_client.create_user(create_user_request)
print("Create user data: ", create_users_response)

# Инициализируем пользовательские данные для аутентификации
authentication_user = AuthenticationUserDict(
    email= create_user_request['email'],
    password= create_user_request['password']
)

# Инициализируем клиент PrivateUsersClient
private_users_client = get_private_users_client(authentication_user)

# Отправляем GET запрос на получение данных пользователя
get_users_response = private_users_client.get_user(create_users_response['user']['id'])
print("Get user data: ", get_users_response)
