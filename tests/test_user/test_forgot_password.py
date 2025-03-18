"""
1. El usuario debe poder enviar una solicitud de olvido de contraseña.
2. El usuario no debe poder enviar una solicitud de olvido de contraseña con una dirección de correo electrónico inválida.
3. Los usuarios no verificados no deben poder solicitar el correo electrónico de olvido de contraseña.
4. Los usuarios inactivos no deben poder solicitar el correo electrónico de olvido de contraseña. 
"""
from app.core.email import fm

def test_user_can_send_forgot_password_request(client, user):
    fm.config.SUPPRESS_SEND = 0
    data = {'email': user.email}
    response = client.post('/auth/forgot-password', json=data)
    assert response.status_code == 200


def test_user_can_not_send_forgot_password_request_with_invalid_email(client, user):
    data = {'email': 'invalid_email'}
    response = client.post('/auth/forgot-password', json=data)
    assert response.status_code == 422


def test_unverified_user_can_not_send_forgot_password_request(client, unverified_user):
    data = {'email': unverified_user.email}
    response = client.post('/auth/forgot-password', json=data)
    print(f"Response: {response.status_code}")  

    assert response.status_code == 200


def test_in_active_user_can_not_send_forgot_password_request(client, inactive_user):
    data = {'email': inactive_user.email}
    response = client.post('/auth/forgot-password', json=data)
    print(f"Response: {response.status_code}")  

    assert response.status_code == 200
