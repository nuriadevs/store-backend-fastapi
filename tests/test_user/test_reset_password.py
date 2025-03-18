from app.core.security import hash_password
from app.utils.email_context import FORGOT_PASSWORD


NEW_PASSWORD = "NuevaaPass_123!"

def _get_token(user):
    string_context = user.get_context_string(context=FORGOT_PASSWORD)
    return hash_password(string_context)

def test_reset_password(client, user):
    data = {
        "token": _get_token(user),
        "email": user.email,
        "password": NEW_PASSWORD
    }
    response = client.put("/auth/reset-password", json=data)
    assert response.status_code == 200
    del data['token']
    del data['email']
    data['username'] = user.email
    login_resp = client.post("/auth/login", data=data)
    assert login_resp.status_code == 200
