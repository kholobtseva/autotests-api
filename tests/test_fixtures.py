import pytest

@pytest.fixture(autouse=True)
def send_analytics_data():
    print("[AUTOUSE] отправляем данные в сервис аналитики")

@pytest.fixture(scope="session")
def settings():
    print("[SESSION] инициализируем настройки автотестов")

@pytest.fixture(scope="class")
def user():
    print("[CLASS] создаем данные пользователя один раз на тестовый класс")

@pytest.fixture(scope="function")
def users_client():
    print("[FUNCTION] Создаем API клиент на каждый автотест")


class TestUserFlow:

    def test_user_can_login(self, settings, user, users_client):
        ...

    def test_user_can_create_course(self, settings, user, users_client):
        ...

class TestAccountFlow:

    def test_user_account(self, settings, user, users_client):
        ...

@pytest.fixture()
def user_date() -> dict:
    print("Создаем пользователя до теста (setup)")
    yield {"username": "test_user", "email": "test@example.com"}
    print("Удаляем пользователя после теста (teardown)")

def test_user_email(user_date: dict):
    print(user_date)
    assert user_date["email"] == "test@example.com"

def test_username(user_date: dict):
    print(user_date)
    assert user_date["username"] == "test_user"