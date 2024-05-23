import allure
import pytest
from Diplom_2.methods.conftest import authorize_user, edit_user, generate_user_credentials, register_user


class TestEditUser:

    @allure.title('Успешное изменение данных пользователя возвращает код 200')
    @pytest.mark.parametrize(
        "new_email,new_password,new_name",
        [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
    )
    def test_edit_authorized_user(self, new_email, new_password, new_name):
        credentials = generate_user_credentials()
        register_user(credentials)
        auth_response = authorize_user(credentials)
        user = auth_response.json()['user']

        # Меняем пользовательские данные
        new_credentials = generate_user_credentials()
        if new_email:
            user['email'] = new_credentials['email']
        if new_password:
            user['password'] = new_credentials['password']
        if new_name:
            user['name'] = new_credentials['name']

        edit_response = edit_user(user, {'Authorization': auth_response.json()['accessToken']})
        assert edit_response.status_code == 200
        assert edit_response.json()['success'] is True
        assert edit_response.json()['user']['email'] == user['email']
        assert edit_response.json()['user']['name'] == user['name']

    @allure.title('Изменение адреса email на другой существующий возвращает код 403')
    def test_edit_authorized_used_with_used_email(self):
        credentials_1 = generate_user_credentials()
        register_user(credentials_1)

        credentials_2 = generate_user_credentials()
        register_user(credentials_2)

        auth_response = authorize_user(credentials_2)
        user = auth_response.json()['user']
        user['email'] = credentials_1['email']

        edit_response = edit_user(user, {'Authorization': auth_response.json()['accessToken']})
        assert edit_response.status_code == 403
        assert edit_response.json()['message'] == 'User with such email already exists'

    @allure.title('Изменение данных пользователя без авторизации возвращает код 401')
    @pytest.mark.parametrize(
        "new_email,new_password,new_name",
        [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
    )
    def test_edit_not_authorized_user(self, new_email, new_password, new_name):
        credentials = generate_user_credentials()
        register_response = register_user(credentials)
        user = register_response.json()['user']


        new_credentials = generate_user_credentials()
        if new_email:
            user['email'] = new_credentials['email']
        if new_password:
            user['password'] = new_credentials['password']
        if new_name:
            user['name'] = new_credentials['name']

        edit_response = edit_user(user)
        assert edit_response.status_code == 401
        assert edit_response.json()['message'] == 'You should be authorised'
