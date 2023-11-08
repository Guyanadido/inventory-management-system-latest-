import datetime
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
import random
from helpers import login_required
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_NAME"] = "my_inventory_app_session"
Session(app)

db = SQL("sqlite:///inventory.db")


@app.route("/")
@login_required
def index():
    dates = [
        'This Month',
        'Today',
        'This Week',
        'This Year',
        'Yesterday',
        'last Week',
        'last Month',
        'last Year',
    ]
    stocks = db.execute(
        "SELECT product_name, quantity FROM inventory_data ORDER BY quantity DESC, selling_price ASC LIMIT 3")
    low_stocks = db.execute(
        "SELECT product_name, quantity FROM inventory_data WHERE low_alert_indicator <= 5 LIMIT 3")
    total_quantity_and_value = db.execute(
        "SELECT sum(selling_price), sum(quantity) FROM inventory_data WHERE status='active'")
    recent_sales = db.execute(
        "SELECT product_name, quantity_sold, total_price FROM sales ORDER BY order_date DESC LIMIT 3")
    return render_template("dashboard.html", stocks=stocks, low_stocks=low_stocks, total_quantity_and_value=total_quantity_and_value[0], dates=dates, recent_sales=recent_sales)


@app.route("/info_based_on_date")
def info():
    q = request.args.get('q')
    column = request.args.get('column')
    current_dates = {
        'This Month': '%Y-%m',
        'Today': '%Y-%m-%d',
        'This Week': '%W',
        'This Year': '%Y',
    }

    past_dates = {
        'Yesterday': ['%Y-%m-%d', '-1 day'],
        'last Week': ['%W', '-7 days'],
        'last Month': ['%Y-%m', '-1 month'],
        'last Year': ['%Y', '-1 year']
    }
    data = []
    if q in current_dates:
        data = db.execute(
            "SELECT SUM(total_price), order_date, product_name FROM sales WHERE strftime(?, order_date) = strftime(?, 'now') GROUP BY product_name ORDER BY ? DESC", current_dates[q], current_dates[q], column)
        return data
    elif q in past_dates:
        data = db.execute(
            "SELECT SUM(total_price), order_date, product_name FROM sales WHERE strftime(?, order_date) = strftime(?, 'now', ?) GROUP BY product_name ORDER BY ? DESC", past_dates[q][0], past_dates[q][0], past_dates[q][1], column)
        return data
    else:
        return


@app.route("/ChartData", methods=["GET", "POST"])
@login_required
def chartData():
    data = db.execute("")


@app.route("/search_item", methods=["GET", "POST"])
@login_required
def search_item():
    q = request.args.get("q")
    table = request.args.get("table")
    column = request.args.get("column")
    if q and table and column:
        items = db.execute(
            "SELECT DISTINCT {} FROM {} WHERE {} LIKE ? LIMIT 20".format(
                column, table, column), "%" + q + "%")
    else:
        items = []
    return items


@app.route("/product", methods=["GET", "POST"])
@login_required
def product():
    if request.method == "POST":
        q = request.form.get("q")
        searched_items = db.execute(
            "SELECT * FROM inventory_data WHERE product_name LIKE ?", "%" + q + "%")
        return render_template("product.html", products=searched_items)

    products = db.execute(
        "SELECT id, product_name, catagory, quantity, selling_price, tax_rate, supplier, stored_location, description FROM inventory_data WHERE status = ?", "active")
    return render_template("product.html", products=products)


@app.route("/AlterTable", methods=["GET", "POST"])
@login_required
def AlterTable():
    if request.method == "POST":
        id = request.form.get("id")
        table = request.form.get("table")
        page = request.form.get("page")
        if id:
            db.execute(
                "UPDATE {} SET status=? WHERE id = ?".format(table), "inactive", id)
    else:
        id = request.args.get("id")
        column = request.args.get("column")
        new_value = request.args.get("value")
        table = request.args.get("table")
        try:
            db.execute("UPDATE {} SET {}=? WHERE id = ?".format(table, column),
                       new_value, id)
        except RuntimeError:
            db.execute("UPDATE {} SET {}=? WHERE person_id = ?".format(table, column),
                       new_value, id)

    if table == "inventory_data":
        return redirect("/product")
    elif table == "sales":
        return redirect("/sales")
    elif page == "supplier":
        return redirect("/supplier")
    else:
        return request("/customers")


@app.route("/newitem", methods=["GET", "POST"])
@login_required
def newitem():
    if request.method == "POST":
        required_inputes = {}
        types = ["Goods", "Services"]

        # validating customer inputs
        # inputs required to be added in the database
        required_inputes["product_type"] = request.form.get("service_type")
        required_inputes["product_name"] = request.form.get("item_name")
        required_inputes["catagory"] = request.form.get("catagory")
        required_inputes["quantity"] = request.form.get("quantity")
        required_inputes["item_description"] = request.form.get(
            "item_description")
        required_inputes["vendor"] = int(request.form.get("Vendor"))
        required_inputes["Brand"] = request.form.get("Brand")
        required_inputes["unit"] = request.form.get("unit")
        required_inputes["purchase_price"] = request.form.get("purchase_price")
        required_inputes["selling_price"] = request.form.get("selling_price")
        required_inputes["purchase_description"] = request.form.get(
            "purchase_description")
        required_inputes["reorder_point"] = request.form.get("reorder_point")
        required_inputes["reorder_quantity"] = request.form.get(
            "reorder_quantity")
        required_inputes["store_location"] = request.form.get("store_location")
        required_inputes["low_stock_indicator"] = int(required_inputes["quantity"]) - \
            int(required_inputes["reorder_point"])
        # inputs not necessarily required to be added in the database
        length = request.form.get("length")
        width = request.form.get("width")
        height = request.form.get("height")
        tax = request.form.get("Tax")

        # making sure if all the required prompts are field
        is_invalid = False
        for input in required_inputes:
            if required_inputes[input] == "":
                is_invalid = True
        if is_invalid == True:
            return "there seems to be unfilled field in the prompts"
        if required_inputes["product_type"] not in types:
            return "invalid product type"

        current_date = datetime.datetime.now().date()
        db.execute("INSERT INTO inventory_data (product_name, product_type, description, catagory, supplier, selling_price, purchase_price, purchase_description ,quantity, reorder_point, reorder_quantity, unit, stored_location, data_added, tax_rate, low_alert_indicator) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   required_inputes["product_name"], required_inputes["product_type"], required_inputes["item_description"], required_inputes["catagory"], required_inputes["vendor"], required_inputes["selling_price"], required_inputes["purchase_price"], required_inputes["purchase_description"], required_inputes["quantity"], required_inputes["reorder_point"], required_inputes["reorder_quantity"], required_inputes["unit"], required_inputes["store_location"], current_date, tax, required_inputes["low_stock_indicator"])

        return redirect("/product")
    return render_template("add_item.html")


@app.route("/sales")
@login_required
def sales():
    searchBy = {
        "product_name": "Product Name",
        "buyer_name": "Customer Name",
        "payment_terms": "Payment Terms",
        "sales_person": "Sales Person",
        "notes_or_comments": "notes/comments",
    }

    sortBy = {
        "0": "Curstomer Name",
        "1": "Product Name",
        "2": "Order Date",
        "3": "Payment Terms",
        "5": "Quantity",
        "6": "Price"
    }
    sales = db.execute(
        "SELECT * FROM sales WHERE status='active'  ORDER BY buyer_name")
    return render_template("sales.html", sales=sales, sortBy=sortBy, searchBy=searchBy)


payment_terms = ['Due on Receipt', 'Net 15', 'Net 30',
                 'Net 45', 'Net 60', 'Due end of the month']


@app.route("/newsale", methods=["GET", "POST"])
@login_required
def newsale():
    if request.method == "POST":
        # required inputes
        product_name = request.form.get("product_name")
        product_id = request.form.get("product_id")
        # product_price = request.form.get("product_price")
        # product_tax = request.form.get("product_tax")
        total_price = request.form.get("product_total_price")
        quantity = request.form.get("quantity")
        customer_name = request.form.get("customer_name")
        customer_id = request.form.get("customer_id")
        payment_term = request.form.get("payment_term")
        valid = product_name and quantity and customer_name and payment_term and product_id and total_price
        if not valid:
            return "some invalid inputs or unkown error recognised please fix them"

        # not nessasarly required inputes
        discount = request.form.get("discount")
        notesOrComments = request.form.get("notes_or_comments")
        todayDate = datetime.datetime.now()
        if len(str(todayDate.day)) == 1:
            todaysday = "0"+str(todayDate.day)
        else:
            todaysday = str(todayDate.day)
        Date = str(todayDate.year) + "-" + \
            str(todayDate.month) + "-" + todaysday
        db.execute(
            "INSERT INTO sales (buyer, order_date, payment_terms, sales_person, Product_id, quantity_sold, total_price, discounts, notes_or_comments, buyer_name, sales_person_name, product_name, status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            customer_id, Date, payment_term, 1, product_id, quantity, total_price, discount, notesOrComments, customer_name, "guyo", product_name, "active")
        return redirect("/sales")

    product_names = db.execute(
        "SELECT DISTINCT id, product_name FROM inventory_data WHERE status = ?", "active")
    customer_names = db.execute(
        "SELECT company, id FROM persons WHERE type = ? GROUP BY company", "customer")
    return render_template("add_sale.html", product_names=product_names, customer_names=customer_names, payment_terms=payment_terms)


@app.route("/salesDetail")
@login_required
def salesDetail():
    query = request.args.get('q')
    product_name = db.execute(
        "SELECT product_name, selling_price ,tax_rate FROM inventory_data WHERE product_name LIKE ? LIMIT 1", "%" + query + "%")
    return product_name


@app.route("/customers")
@login_required
def customers():
    searchBy = [
        "name",
        "company",
        "email"
    ]

    sortBy = {
        "0": "name",
        "1": "company",
        "2": "email",
    }

    buyers = db.execute(
        "SELECT DISTINCT id, name, company, email, work_phone, mobile_phone FROM persons LEFT JOIN phoneNumber ON persons.id = phoneNumber.person_id WHERE type = 'customer' and status='active'")
    return render_template("customers.html", customers=buyers, searchBy=searchBy, sortBy=sortBy)


@app.route("/newcustomers", methods=["POST", "GET"])
@login_required
def newCustomer():
    if request.method == "POST":
        customer_name = request.form.get("customer_name")
        company = request.form.get("company")
        email = request.form.get("email")
        mobile_phone = request.form.get("mobile_phone")
        work_phone = request.form.get("work_phone")

        if customer_name and company and email and mobile_phone and work_phone:
            db.execute("INSERT INTO persons(type, name, company, email) VALUES('customer', ?, ?, ?)",
                       customer_name, company, email)
            id = db.execute("SELECT id FROM persons WHERE name=? AND company=? AND email=?",
                            customer_name, company, email)
            customer_id = id[0]["id"]
            db.execute("INSERT INTO phoneNumber(person_id, work_phone, mobile_phone) VALUES(?, ?, ?)",
                       customer_id, mobile_phone, work_phone)
        else:
            return render_template("error.html", message="Form not properly filled")
    return redirect("/customers")


@app.route("/details")
@login_required
def details():
    id = request.args.get("id")
    buyer = request.args.get("buyer_name")
    table = request.args.get("table")
    if id and buyer and table:
        if table == "persons":
            secondary_people = db.execute(
                "SELECT DISTINCT person_id, name, company, email, work_phone, mobile_phone FROM persons JOIN phoneNumber ON persons.id=phoneNumber.person_id WHERE id IN (SELECT DISTINCT secondary_person FROM secondary_persons WHERE primary_person=?)", id)
            purchase_history = db.execute(
                "SELECT product_name, quantity_sold, order_date, payment_terms, notes_or_comments FROM sales WHERE buyer_name=?", buyer)
            return render_template("customerDetail.html", people=secondary_people, buyer=buyer, purchase_history=purchase_history)
        elif table == "inventory_data":
            purchase_history = db.execute(
                "SELECT id, product_name, description, quantity, purchase_price, stored_location, data_added FROM inventory_data WHERE supplier=? AND status='active'", id)
            return render_template("supplierDetail.html", purchase_history=purchase_history, buyer=buyer)
    return render_template("error.html", message="Id not valid (Customer not found)")


@app.route("/supplier")
@login_required
def suppliers():
    searchBy = [
        "name",
        "company",
        "email"
    ]

    sortBy = {
        "0": "name",
        "1": "company",
        "2": "email",
    }

    vendors = db.execute(
        "SELECT * FROM persons JOIN phoneNumber ON persons.id=phoneNumber.person_id WHERE type='vendor' AND status='active'")
    return render_template("supplier.html", vendors=vendors, searchBy=searchBy, sortBy=sortBy)


@app.route("/purchase")
@login_required
def purchase():
    return render_template("purchase.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", message="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if username:
            user = db.execute(
                "SELECT * FROM users WHERE username = ?", username)
            if len(user) != 0:
                return render_template("error.html", message="user name exist")
        else:
            return render_template("error.html", message="Missing username")

        if not (password and confirmation) or password != confirmation:
            return render_template("error.html", message="empty password field or mismatch")
        else:

            db.execute("INSERT INTO users(username, hash) VALUES(?,?)",
                       username, generate_password_hash(password))
            rows = db.execute("SELECT * FROM users WHERE username = ?",
                              request.form.get("username"))
            session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")
