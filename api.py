from flask import Flask, jsonify, request
from flask_cors import CORS

from database import get_connection


app = Flask(__name__)

CORS(app)

@app.route("/contacts", methods=["GET"])
def get_contacts():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            Id,
            Name,
            Email,
            StartDate,
            IsActive,
            TopicId
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
            "startDate": row[3],
            "isActive": bool(row[4]),
            "topicId": row[5]
        })

    cursor.close()
    connection.close()

    return jsonify(contacts)

@app.route("/topics", methods=["GET"])
def get_topics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            Id,
            Name
        FROM Topics
        WHERE IsActive = 1
        ORDER BY Name
    """)

    rows = cursor.fetchall()

    topics = []

    for row in rows:

        topics.append({
            "id": row[0],
            "name": row[1]
        })

    cursor.close()
    connection.close()

    return jsonify(topics)

@app.route("/contacts", methods=["POST"])
def add_contact():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    start_date = data.get("startDate")
    is_active = data.get("isActive", True)
    topic_id = data.get("topicId")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Contacts
        (
            Name,
            Email,
            StartDate,
            IsActive,
            TopicId
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        email,
        start_date,
        int(is_active),
        topic_id
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Contact added successfully"
    }), 201

@app.route("/contacts/<int:id>", methods=["PUT"])
def update_contact(id):

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    start_date = data.get("startDate")
    is_active = data.get("isActive", True)
    topic_id = data.get("topicId")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE Contacts
        SET
            Name = ?,
            Email = ?,
            StartDate = ?,
            IsActive = ?,
            TopicId = ?
        WHERE Id = ?
    """, (
        name,
        email,
        start_date,
        int(is_active),
        topic_id,
        id
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Contact updated successfully"
    })

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

    return jsonify({
        "message": "Contact deleted successfully"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)