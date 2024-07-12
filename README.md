# Flask REST API

This project implements a REST API using Flask. It includes APIs for user management, item management, login, and logout functionalities. The architecture is designed to be easily extensible for any generic REST API needs.

## Features

- **User Management**
  - Create, retrieve, update, and delete users.
  - Secure endpoints with JWT authentication.

- **Item Management**
  - Create, retrieve, update, and delete items.
  - Support for filtering items based on various conditions.

- **Authentication**
  - Login and receive a JWT token.
  - Logout and invalidate the JWT token.

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Create a virtual environment and install dependencies:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    Create a `.flaskenv` file in the root directory with the following content:

    ```plaintext
    FLASK_APP=app.py
    FLASK_ENV=development
    ```

4. **Run the application:**

    ```sh
    flask run
    ```

5. **Access the API documentation:**

    The Swagger UI is available at [http://localhost:5000/swagger-ui](http://localhost:5000/swagger-ui).

## API Endpoints

### User Management

- **GET /user** - Retrieve all users or a specific user by ID.
- **POST /user** - Add a new user.
- **PUT /user** - Update an existing user.
- **DELETE /user** - Delete a user.

### Item Management

- **GET /item** - Retrieve all items or a specific item by ID.
- **POST /item** - Add a new item.
- **PUT /item** - Update an existing item.
- **DELETE /item** - Delete an item.

### Authentication

- **POST /login** - Login and receive a JWT token.
- **POST /logout** - Logout and invalidate the JWT token.

## Extensibility

The project is designed to be easily extensible. You can add new resources or modify existing ones by following the established patterns. The use of Flask-Smorest for creating blueprints and handling request validation and response formatting makes it easy to extend the API.
