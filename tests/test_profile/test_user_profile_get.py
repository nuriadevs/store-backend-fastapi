  
def test_fetch_user_profile_detail_by_id(auth_client_for_admin, user_profile):

    response = auth_client_for_admin.get(f"/users/profile/{user_profile.user_id}")

    if response.status_code != 200:
        print(f"Respuesta del servidor: {response.text}\n")

    assert response.status_code == 200
    json_response = response.json()
    print(f"Perfil obtenido: {json_response}")

