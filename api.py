import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from mssql_python import connect

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_connection():
    connection_string =(
        f"Server={os.getenv('DB_SERVER')};"
        f"Database={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "Encrypt=no;"
    )

    return connect(connection_string)

@app.route('/contacts', methods=["GET"])
def get_contacts():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT Id, Name, Email, StartDate, IsActive
        FROM Contacts
        ORDER BY Id
""")

    rows = cursor.fetchall()

    contacts = []

    for row in rows:
        contacts.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "startDate": row[3].isoformat(),
            "isActive": bool(row[4])
        })

        cursor.close()
        connection.close()

        return jsonify(contacts)

@app.route("/contacts", methods=["POST"])
def add_contact():
    data = request.get_json()

    name = data["name"]
    email = data["email"]
    start_date = data["startDate"]
    is_active = data["isActive"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Contacts
        (
            Name,
            Email,
            StartDate,
            IsActive
        )
        VALUES (?, ?, ?, ?)
""", (name, email, start_date, is_active))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Contact added successfully"}), 201

@app.route("/contacts/<int:id>", methods=["PUT"])
def update_contact(id):
    data = request.get_json()

    name = data["name"]
    email = data["email"]
    start_date = data["startDate"]
    is_active = data["isActive"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE Contacts
        SET
            Name = ?,
            Email = ?,
            StartDate = ?,
            IsActive = ?
        WHERE Id = ?
""", (
    name, email, start_date, is_active, id
))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Contact updated successfully"}), 200

@app.route("/contacts/<int:id>", methods=["DELETE"])
def delete_contact(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM Contacts
        WHERE Id = ?
""", (id,))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Contact deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)