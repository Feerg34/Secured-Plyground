from flask import Flask, render_template, request, redirect, url_for, session

import secrets, os, mysql.connector 
from dotenv import load_dotenv

load_dotenv()
from database import get_connection

def create_app(): 

    # Create the Flask application
    app = Flask(__name__)

    # os.getenv("SECRET_KEY") read the secret key form .env and app.config["SECRET_KEY"] saves value in Flask configuration
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


    #set route to main page in this example loginPage.html
    # handle the login form submitted using the POST method
    @app.route("/",methods=["POST", "GET"])
    def login():
        if request.method == "GET":
            return render_template("loginPage.html")

        elif request.method == "POST":
            #retreive data entered by the user
            username = request.form["username"]
            password = request.form["password"]

            # rules of connection with database that are is database.py file
            connection = get_connection()
            try:
                if connection is not None:
                    # Cursor is a element form mysql biblioteke that allow to make request to database and receive it
                    cursor = connection.cursor()

                    # it is actually a request that ask for username and password
                    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

                    # this execute the request above
                    cursor.execute(query)

                    # cursor.fetchone() is collecting record form request in my example username
                    user = cursor.fetchone()

                    # i'm closing allowing requests because i already have request and don't need more
                    cursor.close()

                    # if username is not in database return error
                    if user is None:
                        error = "Incorrect username or password"
                        return render_template("loginPage.html", error = error)
                    
                    else:
                        # Sesion = True is required to login, user can reach that only by entering correct data
                        session["logged_in"] = True
                        return redirect(url_for("success_page"))                        
  
                else:

                    error = "Login is temporarily unavailable. Please try again later..."
                    return render_template("loginPage.html", error = error) 
                
            # this code means that even if some returns will be runed connection anyway will be closed
            finally:
                if connection is not None:
                    connection.close()

    # display succes page only if user is logged in
    @app.route("/success")
    def success_page():

        # check if session have logged in status, otherwise it send you to main login page
        if session.get("logged_in"): 
            return render_template("SuccessfullLoginPage.html")
        else:
            return redirect(url_for("login"))   


    # handle the logout button request  
    @app.route("/logout")
    def logout():

        # remove the login status from the user session and redirect the user to login page
        session["logged_in"] = False
        return redirect(url_for("login"))
    
    
    # return the configured Flask application
    return app

# run the application
if __name__ == '__main__':
    app = create_app()

    # start the development server on port 5555
    app.run(host = "0.0.0.0", debug =True, port = 5555)