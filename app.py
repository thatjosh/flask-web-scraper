import os

from cs50 import SQL
from flask import Flask, flash, url_for, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required
from webscrape import bswebscrape, data_clean, webscrapedb_delete, webscrapedb_update

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///webscrape.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=['GET'])
def docscrape():
   """Homepage"""

   # User reach page via GET request
   if request.method == "GET":

      # Store sessions
      return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password matches
        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("passwords must match", 400)

        # Check if user is in database
        input_name = request.form.get("username")
        data_check = db.execute("SELECT * FROM users WHERE username = ?", input_name)
        if data_check:
            return apology("name already exists!", 400)

        # Store user & password in database
        user_name = request.form.get("username")
        user_password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", user_name, user_password)

        # Redirect to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["username"] = rows[0]["username"]

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


@app.route("/pagescrape", methods=['GET', 'POST'])
def pagescrape():
   """Web Scrape Pages"""

   # User reach page via GET request - manually typing address
   if request.method == "GET":

      # Clear sessions
      data = webscrapedb_delete()
      return render_template("pagescrape.html")

   else:
      html_address = request.form.get("htmladdress")
      session["html_address"] = html_address

      # User submitted a POST request (redirect to pagescraped.html)
      return redirect(url_for("/pagescraped"))


@app.route("/pagescraped", methods=['GET', 'POST'])
def pagescraped():
   """Display Results"""

   # User reach page via GET request - redirect to pagescrape
   if request.method == "GET":
      return redirect("/pagescrape")

   else:
      pagescraped = request.form.get("submit")

      # User reach page via POST request (submitted a form in pagescrape.html)
      if not pagescraped:

         # Apology if HTML Address is empty
         html_address = request.form.get("htmladdress")
         session["html_address"] = html_address
         if not html_address:
            return apology("must provide HTML", 400)

         # Run pagescaped if HTML Address is not empty
         else:
            webscraped_data = bswebscrape(html_address)

            # Apology if HTML Address is unsuccessful
            if webscraped_data == 1:
                return apology("invalid HTML address!", 400)

            # Store webscraped_data in session
            session["webscraped_data"] = webscraped_data

            # Date Time
            current_datetime = datetime.datetime.now()
            current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # Store into history if logged on
            key = "username"
            if key in session.keys():
                sqlcmd = db.execute("INSERT INTO records (username, sitelink, datetime) VALUES(?, ?, ?)", session["username"], html_address, current_datetime)

            # Store to file
            session["webscraped_data"] = webscraped_data
            save_path = "/workspaces/74296152/migration/project/static"
            file_name = "webscrape.txt"
            completeName = os.path.join(save_path, file_name)
            file = open(completeName, "w")
            for data in webscraped_data:
                file.write(data)
                file.write("\n")
                file.write("\n")
            file.close()

            return render_template("pagescraped.html", html_address=html_address, webscraped_data=webscraped_data, file=file)

      # User reach page via POST request (submitted a form --> download file)
      else:
        webscraped_data = bswebscrape(html_address)
        return render_template("pagescraped.html", html_address=html_address, webscraped_data=webscraped_data, file=file)


@app.route("/analysed", methods=['GET', 'POST'])
def analysed():
   """Analyse webscraped"""

   # User reach page via GET request - redirect to homepage
   if request.method == "GET":
      return redirect("/")

   # User reach page via POST request (submitted a form)
   else:
      # Analyse data
      cleaned_data = data_clean(session["webscraped_data"])
      webscrapedb_update(cleaned_data["Data"])
      return render_template("analysed.html", webscraped_data=(session["webscraped_data"]), wordcount=cleaned_data["WordCount"])


@app.route("/history", methods=['GET', 'POST'])
@login_required
def history():
    """Display History"""

    if request.method == "GET":
        records = db.execute("SELECT * FROM records WHERE username =?", session["username"])
        count = 1

        if records:
            for record in records:
                record.update({"count": count})
                count += 1
            return render_template("history.html", records=records)
        else:
            return render_template("empty.html")

    # Send to pagscraped
    if request.method == "POST":
        html_address = request.form.get("htmladdress")
        session["html_address"] = html_address
        return redirect(url_for("/pagescraped"))
