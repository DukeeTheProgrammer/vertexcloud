# VertexCloud API: Secure File Storage and Management ☁️

## Overview
VertexCloud API is a robust backend service built with Python and Django, designed for secure user authentication and efficient cloud-based file storage and retrieval. It leverages Django's powerful ORM with SQLite for data persistence, offering a reliable foundation for managing digital assets.

## Features
- **User Authentication**: Secure user registration, login, and session management using Django's built-in authentication system.
- **Session Key Generation**: Dynamic session key generation for authorized API access, ensuring controlled resource interaction.
- **File Upload & Storage**: Endpoints for authenticated users to upload and securely store various file types.
- **File Retrieval**: Capabilities to list all uploaded files for a user or retrieve a specific file by its unique identifier.
- **File Management**: Functionality to delete individual files or clear all user data and sessions.
- **API Health Check**: A simple endpoint to monitor the API's operational status.

## Getting Started

### Installation
To get a local copy up and running, follow these simple steps.

1.  **Clone the Repository**:
    ```bash
    git clone git@github.com:DukeeTheProgrammer/vertexcloud.git
    cd vertexcloud
    ```

2.  **Create a Virtual Environment**:
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**:
    *   **On Windows**:
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies**:
    Install all required packages using pip.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run Migrations**:
    Apply database migrations to set up the necessary tables.
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser (Optional but Recommended)**:
    This allows access to the Django admin panel.
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set up your admin credentials.

7.  **Run the Development Server**:
    Start the Django development server.
    ```bash
    python manage.py runserver
    ```
    The API will be accessible at `http://127.0.0.1:8000/`.

### Environment Variables
While this project does not explicitly use `.env` files, it's crucial for production deployments to manage sensitive information. For local development, `settings.py` has a hardcoded `SECRET_KEY`. **For production, this should be moved to an environment variable.**

| Variable Name | Example Value                                         | Description                                                    |
| :------------ | :---------------------------------------------------- | :------------------------------------------------------------- |
| `SECRET_KEY`  | `'django-insecure-joc65kijw7uby+^-j@z1=yx@j&@a$9=0*t^...'` | Django secret key for cryptographic signing. **CRITICAL for security.** |
| `DEBUG`       | `False`                                               | Controls Django's debug mode. Set to `False` in production.    |
| `ALLOWED_HOSTS` | `['yourdomain.com', 'www.yourdomain.com']`            | A list of strings representing the host/domain names that this Django site can serve. Set to `['*']` for local. |

## API Documentation

### Base URL
The API is served from the root path. For local development, this is typically `http://127.0.0.1:8000/`.

### Endpoints

#### GET /
**Overview**: Checks the health and status of the API.
**Request**: No payload required.
**Response**:
```json
{
  "status": true,
  "request method": "GET",
  "message": "Api is Running Correctly!",
  "runtime": "Active",
  "producer": "DukeeTheProgrammer"
}
```
**Errors**:
- `405 Method Not Allowed`: If a method other than GET is used.

#### POST /signup/
**Overview**: Registers a new user account.
**Request**:
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "StrongPassword123!"
}
```
**Response**:
```json
{
  "status": true,
  "session": true,
  "session_name": "current_user",
  "message": "New User newuser has been created successfully",
  "your session key": "randomstring123new"
}
```
**Errors**:
- `200 OK`: `{"status": false, "message": "Username already Exists"}`
- `200 OK`: `{"status": false, "message": "Email Already Exists"}`
- `405 Method Not Allowed`: If a method other than POST is used.

#### POST /login/
**Overview**: Authenticates an existing user and creates a session.
**Request**:
```json
{
  "username": "existinguser",
  "password": "CorrectPassword123!"
}
```
**Response**:
```json
{
  "status": true,
  "session": true,
  "session_name": "current_user",
  "logged_in": true,
  "user": "existinguser",
  "session_key": "anotherrandomstring456existing"
}
```
**Errors**:
- `200 OK`: `{"status": false, "message": "A severe Error Occured. Could not log you in. Try again", "current_user_status": false}` (Indicates invalid credentials)
- `405 Method Not Allowed`: If a method other than POST is used.

#### POST /token/
**Overview**: Retrieves an existing session key for an authenticated user or generates a new one.
**Request**:
```json
{
  "username": "authenticateduser",
  "password": "CorrectPassword123!"
}
```
**Response**:
```json
{
  "status": true,
  "message": "Your Existing Key is still available",
  "key": "existingrandomstring789auth"
}
```
Or if no key exists:
```json
{
  "status": true,
  "message": "A new key has been created for you",
  "details": {
    "user": "authenticateduser",
    "key": "newrandomstring012user"
  }
}
```
**Errors**:
- `200 OK`: `{"status": false, "message": "Invalid username or password!"}`
- `405 Method Not Allowed`: If a method other than POST is used.

#### POST /create/file/
**Overview**: Uploads a new file for the authenticated user. Requires a valid session key.
**Request**: Form-data (multipart/form-data)
- `file`: (File) The file to be uploaded.
- `key`: (String) The user's session key.
**Response**:
```json
{
  "status": true,
  "message": "File Created Successfully! and has been saved.",
  "file_type": "image/jpeg",
  "filename": "my_picture.jpg",
  "size": 123456
}
```
**Errors**:
- `200 OK`: `{"status": false, "message": "Could not create file : -'filename.ext' - due to Invalid Key! #if you need a new key, use this endpoint '/token/' and register a new key or check if you have an existing one.", "producer": "DukeeTheProgrammer"}`
- `405 Method Not Allowed`: If a method other than POST is used.

#### POST /get/files/
**Overview**: Retrieves a list of all files uploaded by the authenticated user. Requires a valid session key.
**Request**:
```json
{
  "key": "your_session_key"
}
```
**Response**:
```json
{
  "file": {
    "document.pdf": {
      "id": 1,
      "url": "/media/cloud/media/static/files/document.pdf",
      "type": "application/pdf",
      "size": 500000,
      "created_at": "2025-01-01T12:00:00.000Z"
    },
    "image.png": {
      "id": 2,
      "url": "/media/cloud/media/static/files/image.png",
      "type": "image/png",
      "size": 150000,
      "created_at": "2025-01-01T12:05:00.000Z"
    }
  }
}
```
**Errors**:
- `200 OK`: `{"status": false, "message": "Invalid Key entered For this user. You can use /token/ endpoint to create a new key"}`
- `200 OK`: `{"status": false, "message": "No file is available under this User", "authorization": "user-token"}`
- `200 OK`: `{"status": false, "message": "User credentail is not valid for this Operation"}`
- `405 Method Not Allowed`: If a method other than POST is used.

#### GET /get/file/?id=<file_id>&token=<session_key>
**Overview**: Retrieves details for a specific file by its ID. Requires a valid session key as a query parameter.
**Request**: Query Parameters
- `id`: (Integer) The ID of the file to retrieve.
- `token`: (String) The user's session key.
**Response**:
```json
{
  "file": {
    "document.pdf": {
      "id": 1,
      "url": "/media/cloud/media/static/files/document.pdf",
      "type": "application/pdf",
      "size": 500000,
      "created_at": "2025-01-01T12:00:00.000Z"
    }
  }
}
```
**Errors**:
- `200 OK`: `{"status": false, "message": "Invalid Token or Did you forget to add your token to your parameters?"}`
- `200 OK`: `{"status": false, "message": "Invalid Token Key. you can visit '/token/' for a new token key or get your existing ones"}`
- `200 OK`: `{"status": false, "message": "File matching query does not exist."}` (If ID is invalid/not found)
- `405 Method Not Allowed`: If a method other than GET is used.

#### GET /delete/file/?id=<file_id>&key=<session_key>
**Overview**: Deletes a specific file by its ID. Requires the user to be authenticated and provide a valid session key as a query parameter.
**Request**: Query Parameters
- `id`: (Integer) The ID of the file to delete.
- `key`: (String) The user's session key.
**Response**:
```json
{
  "status": true,
  "message": "File with id : '1' has been deleted",
  "authorization": "user-token"
}
```
**Errors**:
- `200 OK`: `{"status": false, "message": "Route is locked due to No login credentials Found. Login to contnue"}`
- `200 OK`: `{"status": false, "message": "Invalid Token Key."}`
- `200 OK`: `{"status": false, "message": "Invalid Token key"}` (If user not found)
- `200 OK`: `{"status": false, "message": "Could not delete file due to File not exists or invalid id given"}`
- `405 Method Not Allowed`: Although `views.py` has a POST handler for this, it explicitly advises to use GET.

#### GET|POST /clear/session/
**Overview**: Flushes the current user's session and logs them out. Requires a valid session key.
**Request**: Query Parameter (for GET) or JSON Body (for POST)
- `key`: (String) The user's session key.
**Response**:
```json
{
  "status": true,
  "message": "User : authenticateduser sessions has been Flushed and Now logged out."
}
```
**Errors**:
- `200 OK`: `{"status": false, "message": "Invalid token Key"}`
- `200 OK`: `{"status": false, "message": "A token is required to access this Endpoint"}`

#### GET|POST /delete/user/
**Overview**: Deletes the authenticated user's account and flushes all associated sessions. Requires authentication, a valid session key, and the user's password.
**Request**: Query Parameters (for GET) or JSON Body (for POST)
- `key`: (String) The user's session key.
- `password`: (String) The user's password.
**Response**:
```json
{
  "status": true,
  "message": "User has been Deleted Successfully and all corresponding sessions has been flushed"
}
```
**Errors**:
- `200 OK`: `{"status": false, "message": "You are not authorized to access this route, you must first be logged in"}`
- `200 OK`: `{"status": false, "message": "Invalid Key Credential"}`
- `200 OK`: `{"status": false, "message": "Invalid User Credentials"}`
- `200 OK`: `{"status": false, "message": "User details is invalid"}`

## Usage
After setting up the project and running the development server, you can interact with the API using tools like `curl`, Postman, or HTTPie. Remember that most endpoints require a session key obtained after `login` or `my_key`.

**Example: Creating a User**
```bash
curl -X POST http://127.0.0.1:8000/signup/ \
-d "username=testuser" \
-d "email=test@example.com" \
-d "password=MySecurePass123"
```
You will receive a response including your `session_key`.

**Example: Logging In**
```bash
curl -X POST http://127.0.0.1:8000/login/ \
-d "username=testuser" \
-d "password=MySecurePass123"
```
This will also provide you with your `session_key` if successful.

**Example: Uploading a File**
Assuming you have a `session_key`:
```bash
curl -X POST -F "file=@/path/to/your/image.jpg" \
-F "key=your_session_key" \
http://127.0.0.1:8000/create/file/
```

**Example: Getting All Files**
```bash
curl -X POST http://127.0.0.1:8000/get/files/ \
-d "key=your_session_key"
```

**Example: Deleting a File**
Replace `1` with the actual file ID and `your_session_key` with your key.
```bash
curl -X GET "http://127.0.0.1:8000/delete/file/?id=1&key=your_session_key"
```

## Technologies Used

| Technology         | Description                                                 | Link                                             |
| :----------------- | :---------------------------------------------------------- | :----------------------------------------------- |
| Python             | The core programming language.                              | [Python](https://www.python.org/)                |
| Django             | High-level Python web framework for rapid development.      | [Django](https://www.djangoproject.com/)         |
| SQLite             | Lightweight, serverless database for development.           | [SQLite](https://www.sqlite.org/index.html)      |
| Whitenoise         | Middleware for serving static files in production.          | [Whitenoise](http://whitenoise.evans.io/)        |
| Gunicorn           | WSGI HTTP Server for UNIX.                                  | [Gunicorn](https://gunicorn.org/)                |
| Requests           | HTTP library for making requests (client-side).             | [Requests](https://requests.readthedocs.io/)     |
| Asgiref / Channels | ASGI tools for asynchronous support.                        | [ASGI](https://asgi.readthedocs.io/)             |
| Pillow             | Imaging library for Python (dependency for Django's FileField). | [Pillow](https://python-pillow.org/)             |

## Contributing
We welcome contributions to enhance VertexCloud API! To contribute:

1.  🍴 **Fork the repository** on GitHub.
2.  🌿 **Create a new branch** for your features or bug fixes: `git checkout -b feature/your-feature-name`.
3.  💻 **Make your changes** and ensure they align with the project's coding style.
4.  🧪 **Write and run tests** to verify your changes: `python manage.py test`.
5.  ➕ **Commit your changes** with a clear and concise message: `git commit -m "feat: Add new awesome feature"`.
6.  ⬆️ **Push your branch** to your forked repository: `git push origin feature/your-feature-name`.
7.  🤝 **Open a Pull Request** to the `main` branch of the original repository.

Please ensure your pull requests are focused, well-tested, and include appropriate documentation updates if applicable.

## License
No specific license file was provided with this project. All rights reserved.

## Author Info
Developed with passion by DukeeTheProgrammer.

*   **GitHub**: [@DukeeTheProgrammer](https://github.com/DukeeTheProgrammer)
*   **Email**: `duke2007@gmail.com`
*   **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/yourusername)
*   **Twitter**: [@YourTwitterHandle](https://twitter.com/yourusername)

---
[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Django 5.2.6](https://img.shields.io/badge/Django-5.2.6-darkgreen.svg)](https://www.djangoproject.com/)
[![License: Unlicensed](https://img.shields.io/badge/License-Unlicensed-red.svg)](https://choosealicense.com/licenses/unlicense/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://github.com/DukeeTheProgrammer/vertexcloud/actions)
[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://www.npmjs.com/package/dokugen)