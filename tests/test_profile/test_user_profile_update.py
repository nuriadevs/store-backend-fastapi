
from app.models.user.user_profile import UserProfile

def test_update_user_profile(auth_client, user_profile, test_session):
    """
    Prueba la actualización del perfil de usuario autenticado.
    """

    # Datos de actualización
    payload = {
        "user_id": user_profile.id,
        "first_name": "Pepito",
        "last_name": "Palotes",
        "dni": "01456123X",
        "phone": 987654321,
        "address": "Sesame Street",
        "birth_date": "1980-03-28",
        "city": "Kyoto",
        "zip_code": 29010
    }

    # Hacer la petición PUT con auth_client (ya autenticado)
    response = auth_client.put("/users/profile/update", json=payload)

    if response.status_code != 200:
        print(f"Respuesta del servidor: {response.text}\n")

    # Verificar respuesta
    assert response.status_code == 200  
    json_response = response.json()

    assert json_response["profile"]["first_name"] == payload["first_name"]
    assert json_response["profile"]["last_name"] == payload["last_name"]

    # Verificar en la base de datos
    updated_profile = test_session.query(UserProfile).filter(UserProfile.user_id == user_profile.user_id).first()
    assert updated_profile.first_name == payload["first_name"]
    assert updated_profile.last_name == payload["last_name"]
    print(f"Nuevo nombre y apellidos: ",updated_profile.first_name)
