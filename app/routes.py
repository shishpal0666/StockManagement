from flask import Blueprint, render_template, redirect, url_for, request
from app import create_app

main_bp = Blueprint('main', __name__)

# Route to display all stocks
@main_bp.route('/')
def index():
    conn = create_app().config['DB_CONNECTION']
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM stocks ORDER BY id ASC")
        stocks = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching stocks: {e}")
        stocks = []
    finally:
        cursor.close()
        conn.close()

    return render_template('index.html', stocks=stocks)

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

        conn = create_app().config['DB_CONNECTION']
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO stocks (name, ticker, price) VALUES (%s, %s, %s)",
                (name, ticker, price)
            )
            conn.commit()  # Commit transaction
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
    conn = create_app().config['DB_CONNECTION']
    cursor = conn.cursor()

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
        
        try:
            price = float(price)  # Ensure price is a valid number
        except ValueError:
            return render_template('edit_stock.html', stock=stock, error="Invalid price.")

        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE stocks SET name = %s, ticker = %s, price = %s WHERE id = %s",
                (name, ticker, price, id)
            )
            conn.commit()  # Commit transaction
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
    conn = create_app().config['DB_CONNECTION']
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM stocks WHERE id = %s", (id,))
        conn.commit()  # Commit transaction
    except Exception as e:
        print(f"Error deleting stock: {e}")
        conn.rollback()  # Rollback if there's an error
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('main.index'))
