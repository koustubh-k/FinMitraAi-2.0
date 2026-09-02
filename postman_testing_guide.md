# Postman API Testing Guide for FinMitraAI

This guide provides detailed inputs and expected outputs to test all the key backend API endpoints of the FinMitraAI application using Postman.

## 1. Postman Environment Setup
Before making requests, set up a Postman Environment (e.g., "FinMitra Local") with the following variables to make testing easier:
- `API_BASE_URL`: `http://localhost:8000/api/v1`
- `AUTH_TOKEN`: *(leave empty, will be populated after login)*
- `REFRESH_TOKEN`: *(leave empty, will be populated after login)*
- `PORTFOLIO_ID`: *(leave empty, will be populated after creating a portfolio)*

For all authenticated endpoints, configure Postman's **Authorization** tab:
- **Type**: Bearer Token
- **Token**: `{{AUTH_TOKEN}}`

---

## 2. Authentication (`/auth`)

### Register User
- **Method**: `POST`
- **URL**: `{{API_BASE_URL}}/auth/register`
- **Body** (raw JSON):
  ```json
  {
    "email": "test@example.com",
    "password": "Password123!",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
- **Expected Output** (`201 Created`):
  ```json
  {
    "id": "uuid-string",
    "email": "test@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true
  }
  ```

### Login
- **Method**: `POST`
- **URL**: `{{API_BASE_URL}}/auth/login`
- **Body** (raw JSON):
  ```json
  {
    "email": "test@example.com",
    "password": "Password123!"
  }
  ```
- **Expected Output** (`200 OK`):
  ```json
  {
    "access_token": "eyJhb...",
    "refresh_token": "random_string_here",
    "token_type": "bearer",
    "expires_in": 900
  }
  ```
> [!TIP]
> **Important:** Copy the `access_token` and set it as the value of your `AUTH_TOKEN` environment variable in Postman to access protected routes. Copy the `refresh_token` into `REFRESH_TOKEN`.

### Get Current User (Authenticated)
- **Method**: `GET`
- **URL**: `{{API_BASE_URL}}/auth/me`
- **Expected Output** (`200 OK`): Returns the user object similar to the registration output.
- **Error Output** (`401 Unauthorized`): `"detail": "Could not validate credentials"` if the token is missing or expired.

### Refresh Token
- **Method**: `POST`
- **URL**: `{{API_BASE_URL}}/auth/refresh`
- **Body** (raw JSON):
  ```json
  {
    "refresh_token": "{{REFRESH_TOKEN}}"
  }
  ```
- **Expected Output** (`200 OK`): Returns a new `access_token` and `refresh_token`.

---

## 3. Portfolios (`/portfolios`)

### Create a Portfolio
- **Method**: `POST`
- **URL**: `{{API_BASE_URL}}/portfolios/`
- **Body** (raw JSON):
  ```json
  {
    "name": "My Tech Portfolio",
    "description": "Tech heavy growth portfolio"
  }
  ```
- **Expected Output** (`201 Created`):
  ```json
  {
    "id": "portfolio-uuid",
    "name": "My Tech Portfolio",
    "description": "Tech heavy growth portfolio",
    "user_id": "user-uuid",
    "created_at": "...",
    "updated_at": "..."
  }
  ```
> [!TIP]
> Save the `id` from the response to your `PORTFOLIO_ID` environment variable.

### Add a Transaction (Buy/Sell)
- **Method**: `POST`
- **URL**: `{{API_BASE_URL}}/portfolios/{{PORTFOLIO_ID}}/transactions`
- **Body** (raw JSON):
  ```json
  {
    "symbol": "AAPL",
    "transaction_type": "buy",
    "quantity": 10,
    "price": 150.00,
    "transaction_date": "2023-10-01"
  }
  ```
- **Expected Output** (`201 Created`): Returns the created transaction object.

### Get Portfolio Holdings
- **Method**: `GET`
- **URL**: `{{API_BASE_URL}}/portfolios/{{PORTFOLIO_ID}}/holdings`
- **Expected Output** (`200 OK`):
  ```json
  [
    {
      "symbol": "AAPL",
      "quantity": 10,
      "average_price": 150.00,
      "current_price": 175.50,
      "total_value": 1755.00,
      "total_return": 255.00,
      "return_percentage": 17.0
    }
  ]
  ```

### Get Portfolio Summary
- **Method**: `GET`
- **URL**: `{{API_BASE_URL}}/portfolios/{{PORTFOLIO_ID}}/summary`
- **Expected Output** (`200 OK`): Returns overall `total_value`, `total_cost`, `total_return`, and `return_percentage`.

---

## 4. Market Data (`/market`)
*Note: Depending on your market data provider, these may require valid Finnhub/AlphaVantage API keys in the backend `.env`.*

### Get Stock Quote
- **Method**: `GET`
- **URL**: `{{API_BASE_URL}}/market/quote/AAPL`
- **Expected Output** (`200 OK`):
  ```json
  {
    "symbol": "AAPL",
    "price": 175.50,
    "change": 2.50,
    "change_percent": 1.44,
    "volume": 55000000,
    "latest_trading_day": "2023-10-25"
  }
  ```

### Get Historical Data
- **Method**: `GET`
- **URL**: `{{API_BASE_URL}}/market/history/AAPL?period=1y&interval=1d`
- **Expected Output** (`200 OK`): Returns a list of daily close prices for the past year.

---

## 5. AI Assistant (`/assistant`)

### Chat with the Financial Assistant
- **Method**: `POST`
- **URL**: `{{API_BASE_URL}}/assistant/chat`
- **Body** (raw JSON):
  ```json
  {
    "message": "What is the current outlook for AAPL?",
    "history": [],
    "context": {
      "portfolio_id": "{{PORTFOLIO_ID}}"
    }
  }
  ```
- **Expected Output** (`200 OK`):
  > [!NOTE]
  > Since this endpoint uses Server-Sent Events (SSE) for streaming, Postman might show it as downloading or receiving a stream. You should see chunks of text like `data: {"chunk": "Apple..."}\n\n` arriving sequentially.

---

## 6. Documents (`/documents`)

### Upload a Financial Document
- **Method**: `POST`
- **URL**: `{{API_BASE_URL}}/documents/upload`
- **Body** (form-data):
  - **Key**: `file` (Change Type from Text to File)
  - **Value**: Select a PDF or text document from your computer.
- **Expected Output** (`200 OK`):
  ```json
  {
    "id": "doc-uuid",
    "filename": "Q3-Report.pdf",
    "status": "processed"
  }
  ```

---

## Troubleshooting Checklist
- **401 Unauthorized**: Your token expired (default is 15 minutes). Use `/auth/login` to get a new one or `/auth/refresh` to refresh it.
- **422 Unprocessable Entity**: The JSON payload is missing a required field or has the wrong data type (e.g., passing a string for a number).
- **500 Internal Server Error**: Check the Docker logs (`docker compose logs api`) to see the Python traceback.
