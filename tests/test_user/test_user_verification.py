import time
from app.core.security import hash_password
from app.models.user.user import User
from app.utils.email_context import USER_VERIFY_ACCOUNT

def test_user_account_verification(client, inactive_user, test_session):

    token_context = inactive_user.get_context_string(USER_VERIFY_ACCOUNT)
    token = hash_password(token_context)
    data = {
        "email": inactive_user.email,
        "token": token
    }
    response = client.post('/users/verify', json=data)
    assert response.status_code == 200  # La verificación debe ser exitosa

    activated_user = test_session.query(User).filter(User.email == inactive_user.email).first()
    assert activated_user.is_active is True  # El usuario debe estar activo
    assert activated_user.verified_at is not None  # Debe tener una fecha de verificación


def test_user_link_doesnot_work_twice(client, inactive_user):

    token_context = inactive_user.get_context_string(USER_VERIFY_ACCOUNT)
    token = hash_password(token_context)
    time.sleep(1)  # retraso antes del segundo intento

    data = {
        "email": inactive_user.email,
        "token": token
    }
    
    response = client.post('/users/verify', json=data)
    assert response.status_code == 200  

    # Intentar verificar nuevamente con el mismo token
    response = client.post('/users/verify', json=data)
    assert response.status_code != 200  


def test_user_invalid_token_does_not_work(client, inactive_user, test_session):

    data = {
        "email": inactive_user.email,
        "token": "avvvvvvvcccccffffeeeeeef"  
    }
    response = client.post('/users/verify', json=data)
    assert response.status_code != 200  # La verificación debe fallar

    activated_user = test_session.query(User).filter(User.email == inactive_user.email).first()
    assert activated_user.is_active is False  # El usuario debe seguir inactivo
    assert activated_user.verified_at is None  # No debe haber una fecha de verificación


def test_user_invalid_email_does_not_work(client, inactive_user, test_session):

    token_context = inactive_user.get_context_string(USER_VERIFY_ACCOUNT)
    token = hash_password(token_context)
    
    data = {
        "email": "error@ejemplo.com",  # Email incorrecto
        "token": token
    }
    
    response = client.post('/users/verify', json=data)
    assert response.status_code != 200  # La verificación debe fallar

    activated_user = test_session.query(User).filter(User.email == inactive_user.email).first()
    assert activated_user.is_active is False  # El usuario debe seguir inactivo
    assert activated_user.verified_at is None  # No debe haber una fecha de verificación
