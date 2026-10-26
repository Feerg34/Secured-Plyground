from flask import Flask, render_template, request, redirect, url_for, session
import werkzeug.security
import secrets, os, mysql.connector 
from dotenv import load_dotenv
# load value of .env file (.env is a file where i store SECRET_KEY value)
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
        # retreive data entered by the user #
            username = request.form["username"]
            password = request.form["password"]

            connection = get_connection()
            try:
                if connection is not None:


                    cursor = connection.cursor()
                    query = ("SELECT * FROM users WHERE username = %s")
                    cursor.execute(query, (username,))
                    user = cursor.fetchone()
                    cursor.close()
                    if user is None:
                        error = "Incorrect username or password"
                        return render_template("loginPage.html", error = error)
                    else:
                        user_password = password
                        user_hash_password = user[2]
                        password_status = werkzeug.security.check_password_hash(user_hash_password, user_password)
                        if password_status == True:
                            session["logged_in"] = True
                            return redirect(url_for("success_page"))
                        
                        else:
                            error = "Incorrect username or password"
                            return render_template("loginPage.html", error = error)




                        
                else:

                    error = "Login is temporarily unavailable. Please try again later..."
                    return render_template("loginPage.html", error = error) 
                
            finally:
                if connection is not None:
                    connection.close()

        #     # store the login status in the user's session
        #     session["logged_in"] = True
        #     return redirect(url_for("success_page"))
        # else:

        #     # if data is incorrect it show error message
        #     error = "Incorrect username or password"
        #     return render_template("loginPage.html", error = error)


    # display succes page only if user is logged in
    @app.route("/success")
    def success_page():

        # check if session have logged in status, otherwise it send you to main login page
        if session.get("logged_in"): 
            return render_template("SuccessfullLoginPage.html")
        else:
            return redirect(url_for("login"))   


    # handle the logout request  
    @app.route("/logout")
    def logout():

        # remove the login status from the user's session and redirect the user to login page
        session["logged_in"] = False
        return redirect(url_for("login"))
    
    
    # return the configured Flask application
    return app

# run the application when this file is executed directly
if __name__ == '__main__':
    app = create_app()

    # start the development server on port 5555
    app.run(debug =True, port = 5555)