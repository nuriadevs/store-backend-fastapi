from tests.conftest import USER_NAME, USER_EMAIL, USER_PASSWORD

def test_create_user(client,user_roles):
    data = {
        "username" : USER_NAME,
        "email": USER_EMAIL,
        "password" : USER_PASSWORD
    } 
    response = client.post('/users',json=data)
    print(response.json())  # Imprimir el mensaje de error
    assert response.status_code == 201
    assert "password" not in response.json()
    

