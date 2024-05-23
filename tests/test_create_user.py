import allure
import pytest
from Diplom_2.methods.conftest import generate_user_credentials, register_user


class TestCreateUser:

    @allure.title('Регистрация нового пользователя возвращает код 200')
    def test_create_unique_user(self):
        credentials = generate_user_credentials()
        response = register_user(credentials)
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['user']['email'] == credentials['email']
        assert response.json()['user']['name'] == credentials['name']
        assert 'accessToken' in response.json()
        assert 'refreshToken' in response.json()

    @allure.title('Регистрация уже зарегистрированного пользователя возвращает код 403')
    def test_create_already_existing_user(self):
        credentials = generate_user_credentials()
        register_user(credentials)
        response = register_user(credentials)
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'User already exists'

    @allure.title('Регистрация без заполнения обязательного поля возвращает код 403')
    @pytest.mark.parametrize(
        "exclude_email,exclude_password,exclude_name",
        [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
    )
    def test_create_user_without_required_field(self, exclude_email, exclude_password, exclude_name):
        credentials = generate_user_credentials(exclude_email, exclude_password, exclude_name)
        response = register_user(credentials)
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Email, password and name are required fields'
