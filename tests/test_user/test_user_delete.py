from app.models.user.user import User

def test_delete_user(auth_client_for_admin, user, test_session):

    # Eliminar usuario
    response = auth_client_for_admin.delete(f"/users/{user.id}")

  
    # Verificar respuesta
    assert response.status_code == 200 


    deleted_user = test_session.query(User).filter(User.id == user.id).first()
     
    assert deleted_user.deleted_at is not None
    print(f"\n Usuario eliminado: ", deleted_user.email)
