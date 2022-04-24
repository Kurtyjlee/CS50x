import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Transaction table only has history, not balance, hence querying for shares is not enough
    # GROUP BY will display the groups only and SUM combines all the share values
    stocks = db.execute("SELECT symbol, name, price, SUM(shares) as totalshares FROM transa WHERE user_id = ? GROUP BY symbol HAVING totalshares != 0", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]  # See buy

    total = cash

    # Go through the list of stocks. Total value of all assets
    for stock in stocks:
        total += stock["price"] * stock["totalshares"]

    return render_template("index.html", stocks=stocks, cash=cash, usd=usd, total=total)  # See quote


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        if not stock:
            return apology("Invalid symbol")

        # Try to convert shares into an int. If fail, means input is alphabet.
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Number of shares must be an integer!")

        # Check if shares is a positive integer
        if shares <= 0:
            return apology("Number of shares not valid!")

        user_id = session["user_id"]

        # db.execute will always return a list of dict. [0]["cash"] will return value.
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        # Gets the name and price of stock, and calculate cost.
        stock_name = stock["name"]
        stock_price = stock["price"]
        cost = stock["price"] * shares

        if cash < cost:
            return apology("Not enough cash")
        else:
            # update the cash reminding and insert the entry into transactions
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - cost, user_id)
            db.execute("INSERT INTO transa (user_id, name, shares, price, type, symbol) VALUES(?, ?, ?, ?, ?, ?)",
                        user_id, stock_name, shares, stock_price, "BUY", symbol)
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    historys = db.execute("SELECT type, symbol, price, shares, time FROM transa WHERE user_id = ?", user_id)

    return render_template("history.html", historys=historys, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # Get symbol and look up
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        # check if the stock is valid
        if not stock:
            return apology("Stock symbol does not exist")
        else:
            # stock=stock just transfers stock in python's var to jinja
            # transfer the usd function into html as usd
            return render_template("quoted.html", stock=stock, usd=usd)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Copy database into a variable
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # If password and confirmation password does not match
        if password != confirmation:
            return apology("Password and confirmation does not match")

        # If no username and password in the field
        elif not username or not password:
            return apology("username and/or password field empty")

        elif len(password) < 8:
            return apology("Password has to be more than 8 characters")

        hash = generate_password_hash(password)
        # Try to insert. If username is already present, it will fail. UNIQUE INDEX
        try:
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)
        except:
            return apology("Username has already been taken")

        # redirect them to the main page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Check that the number of shares is a positive number
        if shares <= 0:
            return apology("Shares must be a positive number")

        # Getting the list of price, name and symbol
        stock = lookup(symbol)
        profit = shares * stock["price"]

        # Getting the number of shares owned
        shares_owned = db.execute("SELECT SUM(shares) as totalsharesowned FROM transa WHERE user_id = ? AND symbol = ? GROUP BY symbol",
                                    user_id, symbol)[0]["totalsharesowned"]

        if shares_owned < shares:
            return apology("Insufficient shares to sell")

        # Updating cash balance and inserting transaction into the table
        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + profit, user_id)
        db.execute("INSERT INTO transa (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)",
                    user_id, stock["name"], -shares, stock["price"], "SELL", symbol)
        return redirect("/")
    else:
        # Getting the symbol of stocks owned by user
        symbols = db.execute("SELECT symbol FROM TRANSA WHERE user_id = ? GROUP BY symbol", user_id)
        return render_template("sell.html", symbols=symbols)

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":

        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        # Check for valid password
        if not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            return apology("invalid password")

        new_pass = request.form.get("new_password")
        con_pass = request.form.get("con_password")

        # Checks if new password is valid, confirmation is valid and pass is long enough
        if not new_pass:
            return apology("Enter valid password")
        elif new_pass != con_pass:
            return apology("Password and confirmation does not match")
        elif len(new_pass) < 8:
            return apology("Password has to be more than 8 characters")

        # Hash password then update database
        hash = generate_password_hash(new_pass)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)

        return redirect("/")

    else:
        return render_template("change_password.html")