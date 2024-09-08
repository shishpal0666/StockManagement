# Stock Management System

## Overview

The Stock Management System is a full-stack web application that allows users to manage a list of stocks. Users can perform CRUD (Create, Read, Update, Delete) operations on stocks, where each stock has a name, ticker symbol, and price. This application uses Flask for the backend, PostgreSQL for the database, and basic HTML, CSS, and JavaScript for the frontend.

## Here is a screenshot of the project:
**Home Page**:
![Project Screenshot](/figures/homepage.png)
**Create Page**:
![Project Screenshot](/figures/createstockpage.png)
**Edit Page**:
![Project Screenshot](/figures/editstockpage.png)

## Features

- **Web Interface**:
  - View all stocks
  - Add new stocks
  - Edit existing stocks
  - Delete stocks

- **API Endpoints**:
  - `POST /api/stocks` - Create a new stock
  - `GET /api/stocks` - Get all stocks
  - `GET /api/stocks/<int:id>` - Get a single stock by ID
  - `PUT /api/stocks/<int:id>` - Update a stock by ID
  - `DELETE /api/stocks/<int:id>` - Delete a stock by ID

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL

### Setup

1. **Clone the Repository**:
 ```bash
git clone https://github.com/your-username/stock-management.git 
cd stock-management
```

2. **Create and Activate a Virtual Environment**:
 ```bash
python -m venv venv 
source venv/bin/activate 
source venv\Scripts\activate # On Windows
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Setup PostgreSQL Database**:
- Create a PostgreSQL database named `stock_management`.
- Apply the necessary schema to your database. You can use the following SQL command to create the `stocks` table:
  ```
  CREATE TABLE stocks (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      ticker VARCHAR(10) UNIQUE NOT NULL,
      price NUMERIC NOT NULL
  );
  ```

5. **Configure Database Connection**:
- Edit `config.py` to include your PostgreSQL database credentials:
  ```
  import psycopg2

  DATABASE_URL = 'postgresql://username:password@localhost/stock_management'

  def get_db_connection():
      conn = psycopg2.connect(DATABASE_URL)
      return conn
  ```

6. **Run the Application**:
```bash
python run.py
```


7. **Access the Application**:
- Open your web browser and go to `http://127.0.0.1:5000` to use the web interface.
- Use API tools like `Postman` or `curl` to interact with the API endpoints.

## Acknowledgments

- Flask for the web framework
- PostgreSQL for the database
- Bootstrap for styling

### Notes:
- Replace `'postgresql://username:password@localhost/stock_management'` with your actual PostgreSQL credentials in `config.py`.
- Ensure `requirements.txt` contains all necessary Python packages, such as Flask and psycopg2.
