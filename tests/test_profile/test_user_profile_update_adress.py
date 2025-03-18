


from app.models.user.user_profile import UserProfile


def test_update_user_address(auth_client, user_profile, test_session):
    """
    Prueba la actualización parcial de la dirección del usuario con PATCH.
    """
    print(f"🟢 Intentando actualizar dirección del usuario {user_profile.id}")

    # Datos a actualizar
    update_data = {
        "address": "Calle Nueva 123",
        "city": "Madrid",
        "zip_code": 28001
    }

    # Enviar request PATCH
    response = auth_client.patch(f"/users/profile/{user_profile.user_id}/address", json=update_data)

    # Verificar respuesta
    assert response.status_code == 200

    # Confirmar que los datos se actualizaron en la base de datos
    updated_profile = test_session.query(UserProfile).filter(UserProfile.user_id == user_profile.user_id).first()

    assert updated_profile is not None
    assert updated_profile.address == "Calle Nueva 123"
    assert updated_profile.city == "Madrid"
    assert updated_profile.zip_code == 28001

    print(f"\n✅ Dirección actualizada correctamente: {updated_profile.address} - {updated_profile.city} ({updated_profile.zip_code})")
