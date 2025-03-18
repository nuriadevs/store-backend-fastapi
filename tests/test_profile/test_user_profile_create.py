

def test_create_user_profile(auth_client, user):

    first_name = "Ash"
    # Datos de actualización del perfil
    payload = {
        "user_id": user.id,
        "first_name": first_name,
        "last_name": "Ketchum",
        "dni": "87654321X",
        "phone": 987654321,
        "address": "Pallet Town",
        "birth_date": "1995-05-22",
        "city": "Kanto",
        "zip_code": 12345
    }

    # Hacer la petición POST
    response = auth_client.post("/users/profile/create", json=payload)


    if response.status_code != 201:
        print(f"Respuesta del servidor: {response.text}\n")

    # Verificar respuesta
    json_response = response.json()
    print(f"Perfil creado: ", json_response)
    assert response.status_code == 201
    assert "password" not in json_response  # Asegurar que no se devuelve la contraseña
    
    
 





