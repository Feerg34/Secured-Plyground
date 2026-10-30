from dotenv import load_dotenv
load_dotenv()
from werkzeug.security import generate_password_hash
from database import get_connection

# i created dictionary with names and password same as i created in database
users = {"Pawel": "Password1", "Kamil":"Password2", "Adam":"Password3","Karsten":"Password4"}

# i used same file as in main app.py that define fules of connection
connection = get_connection()
if connection is not None:

    #same ansd in app.py cursor allow to send and recive date with database
    cursor = connection.cursor()

    #this is command to actually update column "password"
    query = ("UPDATE users SET password = %s WHERE username = %s")

    # here i'm creating loop that generate hash for username and updating it to database
    for username, password in users.items():
        hashed_password = generate_password_hash(password)
        cursor.execute(query,(hashed_password, username,))

    connection.commit()
    cursor.close()
    connection.close()