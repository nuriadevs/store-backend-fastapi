
def test_fetch_me(auth_client, user):

    response = auth_client.get("/users/me")
    assert response.status_code == 200
    assert response.json()['email'] == user.email
    
def test_fetch_user_detail_by_id(auth_client, user):
    response = auth_client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()['email'] == user.email
