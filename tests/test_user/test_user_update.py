from app.models.user.user import User




def test_update_user(auth_client, user, test_session):

    # Datos de actualización
    new_username = "pikachu"
    payload = {
        "username": new_username
    }

    # Hacer la petición PUT
    response = auth_client.put("/users/user_id", json=payload)

    assert response.status_code == 200  
    json_response = response.json()

    assert json_response["username"] == new_username 
    assert "password" not in json_response 

    # Verificar en la base de datos
    updated_user = test_session.query(User).filter(User.id == user.id).first()
    assert updated_user.username == new_username 

