from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.exercises.exercises_client import get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.fakers import fake

# Инициализация клиента пользователей
public_users_client = get_public_users_client()

# Создание пользователя (все поля в snake_case)
create_user_request = CreateUserRequestSchema(
    email=fake.email(),
    password="string",
    last_name="string",  # snake_case вместо lastName
    first_name="string",  # snake_case вместо firstName
    middle_name="string"  # snake_case вместо middleName
)
create_user_response = public_users_client.create_user(create_user_request)
print('Create user data:', create_user_response)

# Аутентификация
authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)

# Инициализация клиентов
files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercises_client = get_exercises_client(authentication_user)

# Загрузка файла
create_file_request = CreateFileRequestSchema(
    filename="image.png",
    directory="courses",
    upload_file="./testdata/files/image.png"
)
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

# Создание курса (все поля в snake_case)
create_course_request = CreateCourseRequestSchema(
    title="Python",
    max_score=100,  # snake_case вместо maxScore
    min_score=10,   # snake_case вместо minScore
    description="Python API course",
    estimated_time="2 weeks",  # snake_case вместо estimatedTime
    preview_file_id=create_file_response.file.id,  # snake_case вместо previewFileId
    created_by_user_id=create_user_response.user.id  # snake_case вместо createdByUserId
)
create_course_response = courses_client.create_course(create_course_request)
print('Create course data:', create_course_response)

# Создание задания (все поля в snake_case)
create_exercise_request = CreateExerciseRequestSchema(
    title="task1",
    course_id=create_course_response.course.id,  # snake_case вместо courseId
    max_score=10,  # snake_case вместо maxScore
    min_score=0,   # snake_case вместо minScore
    order_index=1,  # snake_case вместо orderIndex
    description="Description to task1",
    estimated_time="2 hours"  # snake_case вместо estimatedTime
)
create_exercise_response = exercises_client.create_exercise(create_exercise_request)
print('Create exercise data:', create_exercise_response)