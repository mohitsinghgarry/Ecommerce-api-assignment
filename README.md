# E-commerce Backend API 🛍️

A robust and scalable backend API for an e-commerce platform, built with Python, FastAPI, and MongoDB. This project provides core functionalities for managing products and processing customer orders.

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

---

## ✨ Features

- **Product Management**: Create and list products with detailed attributes like name, price, and available sizes.
- **Advanced Filtering**: Search for products by name (partial/regex) and filter by available sizes.
- **Order Processing**: Create customer orders with multiple items and quantities.
- **User-Specific Order History**: Retrieve a complete list of past orders for any given user.
- **Data Aggregation**: Efficiently joins order and product data to provide detailed order information.
- **Pagination**: Built-in `limit` and `offset` controls for all list endpoints.
- **Async Ready**: Built on FastAPI for high performance.
- **Interactive Docs**: Automatic, interactive API documentation via Swagger UI and ReDoc.

---

## 🚀 Live Demo & API Docs

Once deployed, you can access the live, interactive API documentation here:

[**[➡️ Your Live API URL]/docs**](https://ecommerce-api-assignment-2.onrender.com/)


---

## 🛠️ Tech Stack

| Technology | Description |
| :--- | :--- |
| **Python 3.11** | Core programming language. |
| **FastAPI** | A modern, high-performance web framework for building APIs. |
| **MongoDB** | A NoSQL database used for storing product and order data. |
| **Pydantic** | For data validation and settings management. |
| **Gunicorn & Uvicorn** | Production-grade ASGI server for running the application. |
| **Render** | Cloud platform for hosting the application. |

---

## 🗂️ Project Structure

```

ecommerce\_api/
├── .gitignore
├── database.py         \# Handles MongoDB connection and database logic
├── main.py             \# Main FastAPI application entry point
├── models.py           \# Pydantic models for data validation
├── requirements.txt    \# Project dependencies
├── routes.py           \# API endpoint definitions and logic
└── README.md           \# You are here\!

````

---

## API Endpoints

Here is a detailed breakdown of the available API endpoints.

### Products

#### 1. Create a New Product
- **`POST /products`**
- Creates a new product entry in the database.

<details>
<summary><strong>Example Request & Response</strong></summary>

**cURL Request:**
```sh
curl -X 'POST' \
  '[http://127.0.0.1:8000/products](http://127.0.0.1:8000/products)' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Classic T-Shirt",
  "price": 25.50,
  "sizes": [
    { "size": "small", "quantity": 10 },
    { "size": "large", "quantity": 5 }
  ]
}'
````

**Success Response (201 CREATED):**

```json
{
  "id": "687c982d58ff99a7a3ca9b0c"
}
```

\</details\>

#### 2\. List All Products

  - **`GET /products`**
  - Retrieves a paginated list of products. Supports filtering by `name` and `size`.

\<details\>
\<summary\>\<strong\>Example Request & Response\</strong\>\</summary\>

**cURL Request (with filters):**

```sh
# Get all products with "shirt" in the name, available in size "large"
curl -X 'GET' 'http://127.0.0.1:8000/products?name=shirt&size=large&limit=5'
```

**Success Response (200 OK):**

```json
{
  "data": [
    {
      "id": "687c982d58ff99a7a3ca9b0c",
      "name": "Classic T-Shirt",
      "price": 25.50
    }
  ],
  "page": {
    "next": null,
    "limit": 5,
    "previous": null
  }
}
```

\</details\>

### Orders

#### 3\. Create a New Order

  - **`POST /orders`**
  - Creates a new order for a user with specified products and quantities.

\<details\>
\<summary\>\<strong\>Example Request & Response\</strong\>\</summary\>

**cURL Request:**

```sh
curl -X 'POST' \
  '[http://127.0.0.1:8000/orders](http://127.0.0.1:8000/orders)' \
  -H 'Content-Type: application/json' \
  -d '{
  "userId": "user_123",
  "items": [
    { "productId": "687c982d58ff99a7a3ca9b0c", "qty": 2 },
    { "productId": "687c98a458ff99a7a3ca9b0d", "qty": 1 }
  ]
}'
```

**Success Response (201 CREATED):**

```json
{
  "id": "687c9a4ba0ffa1de10a0cf37"
}
```

\</details\>

#### 4\. Get Orders for a User

  - **`GET /orders/{user_id}`**
  - Retrieves a paginated list of all past orders for a specific user, including product details.

\<details\>
\<summary\>\<strong\>Example Request & Response\</strong\>\</summary\>

**cURL Request:**

```sh
curl -X 'GET' 'http://127.0.0.1:8000/orders/user_123'
```

**Success Response (200 OK):**

```json
{
  "data": [
    {
      "id": "687c9a4ba0ffa1de10a0cf37",
      "total": 76.5,
      "items": [
        {
          "productDetails": {
            "id": "687c982d58ff99a7a3ca9b0c",
            "name": "Classic T-Shirt"
          },
          "qty": 2
        },
        {
          "productDetails": {
            "id": "687c98a458ff99a7a3ca9b0d",
            "name": "Sample 2"
          },
          "qty": 1
        }
      ]
    }
  ],
  "page": {
    "next": null,
    "limit": 10,
    "previous": null
  }
}
```

\</details\>

-----

## ⚙️ Setup and Running Locally

Follow these steps to get the project running on your local machine.

**1. Clone the Repository**

```sh
git clone https://github.com/mohitsinghgarry/Ecommerce-api-assignment.git
cd Ecommerce-api-assignment
```

**2. Create and Activate Virtual Environment**

```sh
# Create a virtual environment
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows)
# venv\Scripts\activate
```

**3. Install Dependencies**

```sh
pip install -r requirements.txt
```

**4. Set Up Environment Variables**
You need to connect to a MongoDB database.

  - Get a connection string from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (M0 Free Tier is sufficient).
  - **Important**: Do not hardcode the URI in your code. Instead, you can set it as an environment variable or use a `.env` file (though for this project, updating `database.py` directly is the simplest start).

**5. Run the Application**

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000`.

-----

## ☁️ Deployment on Render

This application is ready to be deployed on **Render**.

1.  Push your code to a GitHub repository.

2.  Create a new **Web Service** on Render and connect your repository.

3.  Use the following settings during setup:

      - **Build Command**: `pip install -r requirements.txt`
      - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:10000 main:app`

    > **Note:** The `-b 0.0.0.0:10000` part is crucial. It tells the server to listen for public traffic on the port Render provides, which is essential for the deployment to succeed.

-----

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
