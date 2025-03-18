# Evoltronic Store
A project focused on an online shop for selling electronic products. You'll find management of products, orders, user authentication, and user registration.

## Index

1. [Features](#features)
2. [Technologies](#technologies)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Tests](#tests)
7. [License](#license)
8. [Contact](#contact)
9. [Summary](#summary)


## Features

- **User Authentication**: Users can register, log in, email verification, and recover passwords.
- **Product Management**: Administrators can add, edit, and delete products.
- **Order Management**: Customers can place orders and view their order details.
- **Product Categories**: Organizes products into categories for easy navigation.
- **Email Sending with Mailpit**: Registration, confirmation via emails.


## Technologies

This project was developed using the following technologies:

- **Python**: version 3.13.0.
- **FastAPI**: version 0.115.8
- **PostgreSQL**:version 16.8
- **Docker**: version 27.3.1
- **SQLAlchemy**: version  2.0.38
- **Pydantic**: version 2.10.6

## Project Structure

The project follows a modular to ensure future scalability. Below is the main directory structure:

``` python
┣ 📂api
┃ ┣ 📂routes
┃ ┃ ┣ 📂admin
┃ ┃ ┣ 📂auth
┃ ┃ ┣ 📂client
┃ ┃ ┗ 📂public
┃ ┗ 📜api.py
┣ 📂core
┣ 📂dependencies
┣ 📂middlewares
┣ 📂models
┃ ┣ 📂category
┃ ┣ 📂order
┃ ┣ 📂product
┃ ┣ 📂user
┃ ┗ 📜__init__.py
┣ 📂responses
┣ 📂schemas
┣ 📂services
┃ ┣ 📂category
┃ ┣ 📂order
┃ ┣ 📂product
┃ ┣ 📜email.py
┃ ┣ 📜user_profile.py
┃ ┗ 📜user.py
┣ 📂templates
┃ ┗ 📂user
┣ 📂utils
┗ 📜main.py
````

## Installation

## Prerequisites

Before getting started, make sure you have the following installed:

- **Docker** 
- **Python** >= 3.8
- **PostgreSQL**

### Installation Instructions

1. Clone this repository:

   ```bash
   git clone https://github.com/nuriadevs/store-backend-fastapi.git
   cd evoltronic_store
2. Build and start the Docker containers:
   ```bash
   docker-compose up --build
3. Run the migrations:
	```bash   
	docker exec -it fastapi_app alembic upgrade head
4. Open the browser to view the routes:
	```bash   
	http://localhost:8000/docs
5. Open the browser to receive the emails:
	```bash   
	http://localhost:8025/
## Usage
Login using the **admin** user provided in the migration
 
### Register a new user (client)
````
POST/users
 {
  "username": "Lolo",
  "email": "lolo@example.com",
  "password": "PassHashed_123!"
}
````

### Create a new product
````
POST/products/create
{
  "name": "Laptop",
  "description": "Laptop Samsung ultra.",
  "price": 800.50,
  "stock": 10,
  "category_id": 1
}
````

## Tests
````
docker-compose exec app pytest
````

## Contact
If you have any questions send me an email.

✉️ [Email](mailto:nuriadevs@gmail.com)

## Summary
- Run the migration to test the application with an admin user.
- Don't forget to create your own .env file for the variables.
- This project is under construction...can be improved.

