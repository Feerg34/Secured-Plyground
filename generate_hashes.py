from dotenv import load_dotenv
load_dotenv()
from werkzeug.security import generate_password_hash
from database import get_connection

users = {"Pawel": "Password1", "Kamil":"Password2", "Adam":"Password3","Karsten":"Password4"}

connection = get_connection()
if connection is not None:
    cursor = connection.cursor()
    query = ("UPDATE users SET password = %s WHERE username = %s")

    for username, password in users.items():
        hashed_password = generate_password_hash(password)
        cursor.execute(query,(hashed_password, username,))
    connection.commit()
    cursor.close()
    connection.close()


# def passwords_hash():
    
#     from database import get_connection

#     while True:

#         password = input("Write password to hash it:")

#         if password == "exit":
#             print("Finished")
#             break

#         hashed_password = generate_password_hash(password)
    
#         print(f"Hash: {hashed_password}")

# passwords_hash()
