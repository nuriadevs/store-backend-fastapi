from app.services.user import _generate_tokens


def test_refresh_token(client, user, test_session):
    data = _generate_tokens(user, test_session)
    header = {
        "refresh-token": data['refresh_token']
    }
    response = client.post("/auth/refresh", json={}, headers=header)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()
