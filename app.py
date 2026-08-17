from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Database connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Home Page
@app.route('/')
def home():
    return redirect(url_for('login'))

# Add Customer Page
@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        plan_id = request.form['plan_id']

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO customers (name, phone, plan_id) VALUES (%s, %s, %s)",
            (name, phone, plan_id)
        )
        db.commit()
        cursor.close()

        flash("Customer added successfully!")
        return redirect('/customers')
    return render_template("add_customer.html")

@app.route('/customers')
@login_required
def view_customers():
    search = request.args.get('search')

    cursor = db.cursor()

    if search:
        query = """
        SELECT customers.customer_id, customers.name, customers.phone,
        plans.plan_name, plans.price, customers.created_at
        FROM customers
        JOIN plans ON customers.plan_id = plans.plan_id
        WHERE customers.name LIKE %s OR customers.phone LIKE %s
        """
        cursor.execute(query, ('%' + search + '%', '%' + search + '%'))
    else:
        query = """
        SELECT customers.customer_id, customers.name, customers.phone,
        plans.plan_name, plans.price, customers.created_at
        FROM customers
        JOIN plans ON customers.plan_id = plans.plan_id
        """
        cursor.execute(query)

    customers = cursor.fetchall()
    cursor.close()

    return render_template("customers.html", customers=customers)

@app.route('/delete_customer/<int:id>')
@login_required
def delete_customer(id):
    cursor = db.cursor()

    try:
        cursor.execute(
            "DELETE FROM customers WHERE customer_id = %s",
            (id,)
        )
        db.commit()

        flash("Customer deleted successfully!", "success")

    except mysql.connector.IntegrityError:
        db.rollback()

        flash(
            "Customer cannot be deleted because billing records exist.",
            "danger"
        )

    finally:
        cursor.close()

    return redirect(url_for('view_customers'))
@app.route('/edit_customer/<int:id>', methods=['GET','POST'])
@login_required
def edit_customer(id):

    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        plan_id = request.form['plan_id']

        cursor.execute("""
        UPDATE customers
        SET name=%s, phone=%s, plan_id=%s
        WHERE customer_id=%s
        """,(name, phone, plan_id, id))

        db.commit()
        cursor.close()

        return redirect('/customers')

    cursor.execute("SELECT * FROM customers WHERE customer_id=%s",(id,))
    customer = cursor.fetchone()

    cursor.close()

    return render_template("edit_customer.html", customer=customer)

# @app.route('/dashboard')
# def dashboard():
#     cursor = db.cursor()

#     cursor.execute("SELECT COUNT(*) FROM customers")
#     total_customers = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM plans")
#     total_plans = cursor.fetchone()[0]

#     cursor.execute("""
#     SELECT SUM(plans.price)
#     FROM customers
#     JOIN plans ON customers.plan_id = plans.plan_id
#     """)
#     total_revenue = cursor.fetchone()[0]

#     cursor.close()

#     return render_template(
#         "dashboard.html",
#         customers=total_customers,
#         plans=total_plans,
#         revenue=total_revenue
#     )
@app.route('/dashboard')
@login_required
def dashboard():

    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM plans")
    total_plans = cursor.fetchone()[0]

    cursor.execute("""
    SELECT SUM(plans.price)
    FROM customers
    JOIN plans ON customers.plan_id = plans.plan_id
    """)
    total_revenue = cursor.fetchone()[0]

    # Customers by plan
    cursor.execute("""
    SELECT plans.plan_name, COUNT(customers.customer_id)
    FROM customers
    JOIN plans ON customers.plan_id = plans.plan_id
    GROUP BY plans.plan_name
    """)

    plan_data = cursor.fetchall()

    labels = [row[0] for row in plan_data]
    values = [row[1] for row in plan_data]

    cursor.close()

    return render_template(
        "dashboard.html",
        customers=total_customers,
        plans=total_plans,
        revenue=total_revenue,
        labels=labels,
        values=values
    )


@app.route('/generate_bill/<int:id>')
@login_required
def generate_bill(id):

    cursor = db.cursor()

    cursor.execute("""
    SELECT plans.price
    FROM customers
    JOIN plans ON customers.plan_id = plans.plan_id
    WHERE customers.customer_id = %s
    """,(id,))

    price = cursor.fetchone()[0]

    cursor.execute("""
    INSERT INTO bills(customer_id, month, amount)
    VALUES(%s, 'March', %s)
    """,(id, price))

    db.commit()
    cursor.close()

    flash("Bill generated successfully!")
    return redirect('/customers')

@app.route('/bills')
@login_required
def view_bills():

    cursor = db.cursor()

    cursor.execute("""
    SELECT bills.bill_id, customers.name, bills.month, bills.amount
    FROM bills
    JOIN customers ON bills.customer_id = customers.customer_id
    """)

    bills = cursor.fetchall()

    cursor.close()

    return render_template("bills.html", bills=bills)

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()

        cursor.execute(
        "SELECT * FROM admin WHERE username=%s AND password=%s",
        (username, password)
        )

        user = cursor.fetchone()

        if user:
            session['logged_in'] = True
            return redirect('/dashboard')

        else:
            return "Invalid Login"

    return render_template("login.html")

@app.route('/logout')
def logout():

    session.pop('logged_in', None)

    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)