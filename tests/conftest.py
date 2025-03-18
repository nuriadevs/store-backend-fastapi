from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import sys
from typing import Generator
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models.order.order import Order
from app.models.order.order_item import OrderItem
from app.models.category.category import Category
from app.models.product.product import Product
from app.models.user.user_roles import UserRole
from app.models.user.user_profile import UserProfile
from app.core.security import generate_token, hash_password
from app.models.user.user import User
from app.main import app
from app.core.database import Base, get_session

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Acceder a las variables de entorno del archivo .env
USER_NAME = os.getenv("USER_NAME")
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")


POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")



DATABASE_URL = f"postgresql://postgres:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Crear la conexión con la base de datos
engine = create_engine(DATABASE_URL)



# Sesión de prueba para las operaciones de la base de datos
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture para crear la sesión de prueba y consultas a la BBDD
@pytest.fixture(scope="function")
def test_session() -> Generator:
    session = SessionTesting()
    print(f"\n🟢 Creando sesión de prueba...")  
    try:
        yield session  
    finally:
        session.rollback() 

        session.close()  
        print(f"\n🔴 Sesión cerrada.")  

# Fixture para preparar la aplicación para las pruebas
@pytest.fixture(scope="function")
def app_test():
    print("Prueba app_test...")
    Base.metadata.create_all(bind=engine)  
    yield app 
    Base.metadata.drop_all(bind=engine) 

# Fixture para autenticar un usuario en las pruebas.
@pytest.fixture(scope="function")
def auth_client(app_test, test_session, user):
    print("Cliente de prueba con autenticación...")
    def _test_db():
        try:
            yield test_session
        finally:
            pass

    # Sobrescribe la dependencia para que use la base de datos de prueba
    app_test.dependency_overrides[get_session] = _test_db

    # Genera el token para el usuario de prueba
    payload = {"sub": str(user.id)}
    token = generate_token(payload, timedelta(minutes=30))

    client = TestClient(app_test)
    client.headers['Authorization'] = f"Bearer {token}"
    client.timeout = 10 
    return client


# Fixture para crear un cliente de prueba para enviar solicitudes HTTP
@pytest.fixture(scope="function")
def client(app_test, test_session):
    def _test_db():
        try:
            yield test_session
        finally:
            pass
    
    app_test.dependency_overrides[get_session] = _test_db 
    return TestClient(app_test) 

# Fixture para crear un cliente inactivo
@pytest.fixture(scope="function")
def inactive_user(test_session):
    model = User()
    model.username = USER_NAME
    model.email = USER_EMAIL
    model.password = hash_password(USER_PASSWORD)
    model.updated_at = datetime.now(timezone.utc)
    model.is_active = False
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model

# Fixture para crear un usuario con rol admin o el que sea
@pytest.fixture(scope="function")
def user(test_session):
    model = User()
    model.username = USER_NAME
    model.email = USER_EMAIL
    model.password = hash_password(USER_PASSWORD)
    model.updated_at = datetime.now(timezone.utc)
    model.verified_at = datetime.now(timezone.utc)
    model.is_active = True

    # Asignar rol 'admin' al usuario (o el rol que sea necesario)
    role = test_session.query(UserRole).filter_by(name="admin").first()
    if not role:
        role = UserRole(name="admin")
        test_session.add(role)
        test_session.commit()

    model.roles = [role] 

    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)

    return model

# Fixture para usuario sin verificar
@pytest.fixture(scope="function")
def unverified_user(test_session):
    model = User()
    model.username = USER_NAME
    model.email = USER_EMAIL
    model.password = hash_password(USER_PASSWORD)
    model.updated_at = datetime.now(timezone.utc)
    model.is_active = True
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model

#Fixture de perfil de usuario asociado al usuario autenticado.
@pytest.fixture(scope="function")
def user_profile(test_session, user):
    profile = UserProfile(
        user_id=user.id,
        first_name="Ash",
        last_name="Ketchum",
        dni="00123123K",
        phone=987654321,
        address="Pallet Town",
        birth_date=datetime(1995, 5, 22),
        city="Kanto",
        zip_code=12345
    )
    test_session.add(profile)
    test_session.commit()
    test_session.refresh(profile)
    return profile

#Fixture que inserta roles en la base de datos de prueba.
@pytest.fixture(scope="function")
def user_roles(test_session):
    roles = ["cliente", "admin"]
    created_roles = []

    for role_name in roles:
        existing_role = test_session.query(UserRole).filter_by(name=role_name).first()
        if not existing_role:
            role = UserRole(name=role_name)
            test_session.add(role)
            test_session.flush()  
            created_roles.append(role)

    test_session.commit()
    return created_roles  


#Fixture que crea una categoría de prueba en la base de datos
@pytest.fixture(scope="function")
def test_category(test_session):

    category = Category(name="Electrónica", description="Productos electrónicos")
    test_session.add(category)
    test_session.commit()
    test_session.refresh(category)
    return category  


#Fixture que crea un producto de prueba con una categoría
@pytest.fixture(scope="function")
def test_product(test_session, test_category):

    product = Product(
        name="Laptop Gamer",
        description="Laptop de alto rendimiento para gaming",
        price=1200.00,
        stock=10,
        category_id=test_category.id,
        deleted_at=None
    )
    test_session.add(product)
    test_session.commit()
    test_session.refresh(product)
    return product

 
#Fixture que crea un pedido de prueba con un usuario.
@pytest.fixture(scope="function")
def test_order(test_session,user):

    order = Order(
        user_id=user.id,
        total_price=0,  
        status="pendiente"
    )
    test_session.add(order) 
    test_session.commit()
    test_session.refresh(order)
    return order


#Fixture que crea un item de pedido de prueba con pedido y productos
@pytest.fixture(scope="function")
def test_order_item(test_session, test_order, test_product):

    order_item = OrderItem(
        order_id=test_order.id,  
        product_id=test_product.id,
        quantity=2,
        subtotal=2400.00  # 2 * 1200.00
    )
    test_session.add(order_item)
    test_session.commit()
    test_session.refresh(order_item)
    return order_item


#Fixture para autenticar un usuario admin en las pruebas
@pytest.fixture(scope="function")
def auth_client_for_admin(app_test, test_session, admin_user):

    def _test_db():
        try:
            yield test_session
        finally:
            pass

    # Sobrescribe la dependencia para que use la base de datos de prueba
    app_test.dependency_overrides[get_session] = _test_db

    # Genera el token para el admin_user
    payload = {"sub": str(admin_user.id)}  
    token = generate_token(payload, timedelta(minutes=30))
    

    client = TestClient(app_test)
    client.headers['Authorization'] = f"Bearer {token}"

    return client


#Fixture que crea un usuario administrador en la base de datos de prueba
@pytest.fixture(scope="function")
def admin_user(test_session):

    admin_role = UserRole(name="admin")
    test_session.add(admin_role)
    test_session.commit()

    admin_user = User(
        username="admin",
        email="admin@example.com",
        password=hash_password(USER_PASSWORD), 
        is_active=True
    )
    
    admin_user.roles = [admin_role]
    
    test_session.add(admin_user)
    test_session.commit()
  
    return admin_user
