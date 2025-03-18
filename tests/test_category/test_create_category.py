
def test_create_category(auth_client_for_admin, test_category):
    
    # Datos de la categoría que vamos a crear
    payload = {
        "name": "Informatica",
        "description": "Todo lo relacionado con Informatica."
    }

    # Hacer la petición POST
    response = auth_client_for_admin.post("/categories/create", json=payload)

    # 🚀 Agregar logs detallados en caso de error
    if response.status_code != 201:
        print(f"Respuesta del servidor: {response.text}\n")


    json_response = response.json()
    print(f"Categoría creada: ", json_response)

    # Verificar que el código de estado sea 201 (creado)
    assert response.status_code == 201

    # Verificar que la categoría se haya creado con los datos correctos
    assert json_response["name"] == payload["name"]
    assert json_response["description"] == payload["description"]
    assert "id" in json_response  # Verificar que se devuelve un ID para la categoría creada
