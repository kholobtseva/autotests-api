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
