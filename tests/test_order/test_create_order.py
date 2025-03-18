from app.models.order.order import Order
from app.models.order.order_item import OrderItem


def test_create_order(auth_client,user, test_product, test_order_item):
     # Datos para la creación del pedido 
    payload = {
        "user_id": user.id,  
        "total_price": float(test_order_item.subtotal),  
        "status": "pendiente", 
        "products": [
        {"product_id": test_product.id, "quantity": 2} 
    ]
    }


    # Hacer la petición POST para crear la orden
    response = auth_client.post("/orders/create/", json=payload)



    if response.status_code != 201:
        print(f"Respuesta del servidor: {response.text}\n")

    # Verificar la respuesta
    json_response = response.json()
    print(f"Orden creada: ", json_response)

    # Verificar que el código de estado sea 201 (creado)
    assert response.status_code == 201

