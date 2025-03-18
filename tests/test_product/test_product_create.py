from app.models.product.product import Product




def test_create_product(auth_client_for_admin, test_session, test_category):
    """
    Prueba la creación de un nuevo producto.
    """
    # Datos del producto a crear
    product_data = {
        "name": "Smartphone Pro",
        "description": "Teléfono inteligente de última generación",
        "price": 899.99,
        "stock": 50,
        "category_id": test_category.id  # Usamos la categoría de prueba
    }

    # Mostrar los datos del producto antes de enviarlos
    print("🟢 Intentando crear un nuevo producto con los siguientes datos:")
    print(product_data)

    # Enviar solicitud a la API
    response = auth_client_for_admin.post("/products/create", json=product_data)

    # Verificar la respuesta
    print(f"✅ Respuesta del servidor: {response.status_code} - {response.text}")

    try:
        assert response.status_code == 201
    except AssertionError as e:
        print(f"Error en la respuesta: {e}")
        raise  # Vuelve a lanzar la excepción para que el test falle

    # Verificar los datos devueltos en la respuesta
    data = response.json()
    print("🟢 Datos devueltos en la respuesta:")
    print(data)

    # Comprobamos que los datos devueltos coinciden con los datos enviados
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["stock"] == product_data["stock"]
    assert data["category_id"] == product_data["category_id"]

    # Verificar que el producto se ha guardado en la base de datos
    created_product = test_session.query(Product).filter_by(name=product_data["name"]).first()
    assert created_product is not None
    assert created_product.name == product_data["name"]
    print(f"✅ Producto creado correctamente en la base de datos: {created_product.name}")
