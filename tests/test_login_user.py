import allure
from Diplom_2.methods.conftest import authorize_user, generate_user_credentials, register_user


class TestLoginUser:

    @allure.title('Успешная авторизация пользователя возвращает код 200')
    def test_login_registered_user(self):
        credentials = generate_user_credentials()
        register_user(credentials)
        response = authorize_user(credentials)
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['user']['email'] == credentials['email']
        assert response.json()['user']['name'] == credentials['name']
        assert 'accessToken' in response.json()
        assert 'refreshToken' in response.json()

    @allure.title('Авторизация незарегистрированного пользователя возвращает код 401')
    def test_login_not_registered_user(self):
        credentials = generate_user_credentials(exclude_name=True)
        response = authorize_user(credentials)
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == "email or password are incorrect"
