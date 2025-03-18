from app.models.user.user_profile import UserProfile



def test_delete_profile_user(auth_client, user_profile, test_session):
    """
    Prueba la eliminación lógica del perfil de usuario.
    """

    # Verificar que el perfil existe antes del DELETE
    existing_profile = test_session.query(UserProfile).filter(UserProfile.user_id == user_profile.user_id).first()

    assert existing_profile is not None
    assert existing_profile.deleted_at is None


    # Eliminar perfil de usuario
    response = auth_client.delete(f"/users/profile/{user_profile.id}")

    # Verificar respuesta
    assert response.status_code == 200

    # Confirmar que el perfil fue marcado como eliminado
    deleted_profile = test_session.query(UserProfile).filter(UserProfile.user_id == user_profile.id).first()

    assert deleted_profile is not None
    assert deleted_profile.deleted_at is not None

