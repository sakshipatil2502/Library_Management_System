**FastAPI Project**
Installation
To get started, install the required dependencies using pip:

bash
Copy
pip install fastapi uvicorn sqlalchemy python-jose python-multipart pytest httpx
Running the Application
To run the FastAPI application, use the following uvicorn command:

bash
Copy
uvicorn main:app --reload
This will start the development server on http://127.0.0.1:8000.

Unit Test cases
bash
Copy
pytest main_test.py

API Endpoint
POST - Register User
URL: http://127.0.0.1:8000/users/register

Request Body:

json
Copy
{
    "email": "email@email.com",
    "name": "username",
    "role": "user",
    "password": "password"
}

venv\Scripts\activate
python -m uvicorn main:app --reload

Step 1: Register Admin
Method: POST

URL: http://127.0.0.1:8000/users/register

Body (JSON):

json

{
  "name": "Admin",
  "email": "admin@example.com",
  "password": "admin123",
  "role": "admin"
}

Step 2: Login (Admin)
Method: POST

URL: http://127.0.0.1:8000/users/login

Body (x-www-form-urlencoded):

username: admin@example.com  
password: admin123 

ADMIN OPERATIONS: 

Step 3: Add New Book
Method: POST

URL: http://127.0.0.1:8000/books/

Headers:
Authorization: Bearer <ADMIN_TOKEN>
Body:

json

{
  "title": "Atomic Habits",
  "author": "James Clear",
  "isbn": "9780735211292",
  "published_year": 2018,
  "category": "Self-help",
  "quantity": 5
}

Step 4: Update a Book
Method: PUT

URL: http://127.0.0.1:8000/books/1

Headers:
Authorization: Bearer <ADMIN_TOKEN>

Body:

json
{
  "title": "Atomic Habits - Updated",
  "author": "James Clear",
  "isbn": "9780735211292",
  "published_year": 2019,
  "category": "Self-help",
  "quantity": 10
}

Step 5: Delete a Book
Method: DELETE

URL: http://127.0.0.1:8000/books/1

Headers:
Authorization: Bearer <ADMIN_TOKEN>

Step 6: List All Users
Method: GET

URL: http://127.0.0.1:8000/books/1

Headers:

Authorization: Bearer <ADMIN_TOKEN>

Step 8: Update a User
Method: PUT

URL: http://127.0.0.1:8000/users/2

Headers:
Authorization: Bearer <ADMIN_TOKEN>
Body:

json

{
  "name": "Updated User",
  "email": "updateduser@example.com"
}

Step 9: Delete a User(by id)
Method: DELETE

URL: http://127.0.0.1:8000/users/2

Headers:

Authorization: Bearer <ADMIN_TOKEN>

Step 10: View Overdue Books
Method: GET

URL: http://127.0.0.1:8000/transactions/overdue

Headers:

Authorization: Bearer <ADMIN_TOKEN>

Step 11: View Borrowed Books
Method: GET

URL: http://127.0.0.1:8000/transactions/borrowed/2

Response: Admin Access required


USER OPERATIONS (Updated Logical Flow)

Step 1: Register User
URL: http://127.0.0.1:8000/users/register

Body (JSON):

json

{
  "name": "User1",
  "email": "user1@example.com",
  "password": "user123",
  "role": "user"
}

Step 2: Login (User)
Method: POST

URL: http://127.0.0.1:8000/users/login

Body (x-www-form-urlencoded):

username:user1@example.com
password:user123

Response:

{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}

Step 3: List All Books
Method: GET

URL: http://127.0.0.1:8000/books/

No token required

Step 4: List Books By Id
Method: GET

URL: http://127.0.0.1:8000/books/1

No token required

Step 5: View Borrowed Books
Method: GET

URL: http://127.0.0.1:8000/transactions/borrowed/2

Response: Admin Access required

Step 6: Checkout Book
Method: POST

URL: http://127.0.0.1:8000/transactions/checkout

Authorization: Bearer <USER_TOKEN>
Body:

json

{
  "user_id": 2,
  "book_id": 1,
  "checkout_date": "2025-04-05",
  "due_date": "2025-04-12"
}

Step 7: Return Book
Method: POST

URL: http://127.0.0.1:8000/transactions/return

Authorization: Bearer <USER_TOKEN>

Body:JSON

{
  "user_id": 2,
  "book_id": 1,
  "return_date": "2025-04-10"
}