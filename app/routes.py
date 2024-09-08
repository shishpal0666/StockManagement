from flask import Blueprint, render_template, redirect, url_for, request, jsonify, abort
from app import create_app
import psycopg2

main_bp = Blueprint('main', __name__)

# Helper function to get a database connection and cursor
def get_db_cursor():
    app = create_app()
    conn = app.config['DB_CONNECTION']
    cursor = conn.cursor()
    return conn, cursor

# Helper function to commit changes and close the connection
def commit_and_close(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()

# Route to display all stocks
@main_bp.route('/')
def index():
    conn, cursor = get_db_cursor()
    try:
        cursor.execute("SELECT * FROM stocks ORDER BY id ASC") # Display in the order of id's
        stocks = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching stocks: {e}")
        stocks = []
    finally:
        commit_and_close(conn, cursor)

    return render_template('index.html', stocks=stocks) # passing stocks to html or templates to display by uning jinja

# Route to add a new stock
@main_bp.route('/add', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        name = request.form['name']
        ticker = request.form['ticker']
        price = request.form['price']

        # Basic validation
        if not name or not ticker or not price:
            return render_template('add_stock.html', error="All fields are required.")
        
        try:
            price = float(price)  # Ensure price is a valid number
        except ValueError:
            return render_template('add_stock.html', error="Invalid price.")

        conn, cursor = get_db_cursor()
        #insertion to the table
        try:
            cursor.execute(
                "INSERT INTO stocks (name, ticker, price) VALUES (%s, %s, %s)",
                (name, ticker, price)
            )
            commit_and_close(conn, cursor)
        except Exception as e:
            print(f"Error adding stock: {e}")
            conn.rollback()  # Rollback if there's an error
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('main.index'))

    return render_template('add_stock.html')

# Route to edit an existing stock
@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_stock(id):
    conn, cursor = get_db_cursor()

    try:
        cursor.execute("SELECT * FROM stocks WHERE id = %s", (id,))
        stock = cursor.fetchone()
    except Exception as e:
        print(f"Error fetching stock: {e}")
        stock = None
    finally:
        cursor.close()

    if request.method == 'POST':
        name = request.form['name']
        ticker = request.form['ticker']
        price = request.form['price']

        # Basic validation
        if not name or not ticker or not price:
            return render_template('edit_stock.html', stock=stock, error="All fields are required.")
            # generate an error of invalid or NA information
        try:
            price = float(price)  # Ensure price is a valid number
        except ValueError:
            return render_template('edit_stock.html', stock=stock, error="Invalid price.")

        conn, cursor = get_db_cursor()

        try:
            cursor.execute(
                "UPDATE stocks SET name = %s, ticker = %s, price = %s WHERE id = %s",
                (name, ticker, price, id) #updation of the stocks
            )
            commit_and_close(conn, cursor)
        except Exception as e:
            print(f"Error updating stock: {e}")
            conn.rollback()  # Rollback if there's an error
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('main.index'))

    return render_template('edit_stock.html', stock=stock)

# Route to delete a stock
@main_bp.route('/delete/<int:id>', methods=['POST'])
def delete_stock(id):
    conn, cursor = get_db_cursor()

    try:
        cursor.execute("DELETE FROM stocks WHERE id = %s", (id,))
        commit_and_close(conn, cursor)
    except Exception as e:
        print(f"Error deleting stock: {e}")
        conn.rollback()  # Rollback if there's an error
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('main.index'))

# API route to create a new stock
@main_bp.route('/api/stocks', methods=['POST'])
def api_create_stock():
    data = request.json
    name = data.get('name')
    ticker = data.get('ticker')
    price = data.get('price')

    if not all([name, ticker, price]):
        abort(400, description="Missing required fields")

    try:
        price = float(price)  # Ensure price is a valid number
    except ValueError:
        abort(400, description="Invalid price")

    conn, cursor = get_db_cursor()

    try:
        cursor.execute(
            "INSERT INTO stocks (name, ticker, price) VALUES (%s, %s, %s)",
            (name, ticker, price)
        )
        commit_and_close(conn, cursor)
        return jsonify({"message": "Stock created"}), 201
    except psycopg2.IntegrityError:
        conn.rollback()  # Rollback if there's an error
        commit_and_close(conn, cursor)
        abort(400, description="Ticker already exists")

# API route to read all stocks
@main_bp.route('/api/stocks', methods=['GET'])
def api_read_stocks():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT * FROM stocks")
    stocks = cursor.fetchall()
    commit_and_close(conn, cursor)

    stocks_list = [
        {"id": stock[0], "name": stock[1], "ticker": stock[2], "price": stock[3]}
        for stock in stocks
    ]
    return jsonify(stocks_list)

# API route to read a single stock by ID
@main_bp.route('/api/stocks/<int:id>', methods=['GET'])
def api_read_stock(id):
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT * FROM stocks WHERE id = %s", (id,))
    stock = cursor.fetchone()
    commit_and_close(conn, cursor)

    if stock is None:
        abort(404, description="Stock not found")

    stock_dict = {
        "id": stock[0],
        "name": stock[1],
        "ticker": stock[2],
        "price": stock[3]
    }
    return jsonify(stock_dict)

# API route to update a stock by ID
@main_bp.route('/api/stocks/<int:id>', methods=['PUT'])
def api_update_stock(id):
    data = request.json
    name = data.get('name')
    ticker = data.get('ticker')
    price = data.get('price')

    if not any([name, ticker, price]):
        abort(400, description="No fields provided to update")

    try:
        price = float(price)  # Ensure price is a valid number
    except ValueError:
        abort(400, description="Invalid price")

    conn, cursor = get_db_cursor()

    try:
        cursor.execute(
            "UPDATE stocks SET name = %s, ticker = %s, price = %s WHERE id = %s",
            (name, ticker, price, id)
        )
        if cursor.rowcount == 0:
            abort(404, description="Stock not found")
        commit_and_close(conn, cursor)
        return jsonify({"message": "Stock updated"})
    except psycopg2.IntegrityError:
        conn.rollback()  # Rollback if there's an error
        commit_and_close(conn, cursor)
        abort(400, description="Ticker already exists")

# API route to delete a stock by ID
@main_bp.route('/api/stocks/<int:id>', methods=['DELETE'])
def api_delete_stock(id):
    conn, cursor = get_db_cursor()
    cursor.execute("DELETE FROM stocks WHERE id = %s", (id,))
    if cursor.rowcount == 0:
        commit_and_close(conn, cursor)
        abort(404, description="Stock not found")

    commit_and_close(conn, cursor)
    return jsonify({"message": "Stock deleted"})
