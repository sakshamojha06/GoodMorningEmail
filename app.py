from datetime import date, timedelta

from database import get_connection
from email_service import send_good_morning_email
from openai_service import generate_fact
from secret_manager_service import get_openai_api_key


def get_daily_fact(cursor, topic, today):

    cursor.execute("""
        SELECT Id, Fact
        FROM DailyFacts
        WHERE Topic = ?
        AND FactDate = ?
    """, (
        topic,
        today.isoformat()
    ))

    row = cursor.fetchone()

    if row:
        print(f"Using existing fact for {topic}")
        return row[0], row[1]

    print(f"Generating new fact for {topic}")

    api_key = get_openai_api_key()

    fact = generate_fact(
        topic,
        api_key
    )

    cursor.execute("""
        INSERT INTO DailyFacts
        (
            Topic,
            FactDate,
            Fact
        )
        VALUES (?, ?, ?)
    """, (
        topic,
        today.isoformat(),
        fact
    ))

    fact_id = cursor.lastrowid

    return fact_id, fact


def send_daily_emails():

    connection = get_connection()
    cursor = connection.cursor()

    print("SQLite database connected successfully!")

    today = date.today()

    cursor.execute("""
        SELECT
            C.Id,
            C.Name,
            C.Email,
            C.StartDate,
            C.IsActive,
            C.TopicId,
            T.Name
        FROM Contacts C
        INNER JOIN Topics T
            ON C.TopicId = T.Id
    """)

    contacts = cursor.fetchall()

    for contact in contacts:

        contact_id = contact[0]
        name = contact[1]
        email = contact[2]
        start_date = date.fromisoformat(contact[3])
        is_active = contact[4]
        topic_id = contact[5]
        topic = contact[6]

        print(f"\nProcessing: {name}")

        if not is_active:
            print(f"Skipping inactive contact: {name}")
            continue

        end_date = start_date + timedelta(days=2)

        if not (start_date <= today <= end_date):
            print(f"Outside 3-day period for {name}")
            continue

        cursor.execute("""
            SELECT COUNT(*)
            FROM EmailLogs
            WHERE ContactId = ?
            AND SentDate = ?
        """, (
            contact_id,
            today.isoformat()
        ))

        log_count = cursor.fetchone()[0]

        if log_count > 0:
            print(f"Email already sent to {name} today.")
            continue

        fact_id, fact = get_daily_fact(
            cursor,
            topic,
            today
        )

        send_good_morning_email(
            name,
            email,
            topic,
            fact
        )

        cursor.execute("""
            INSERT INTO EmailLogs
            (
                ContactId,
                SentDate,
                FactId
            )
            VALUES (?, ?, ?)
        """, (
            contact_id,
            today.isoformat(),
            fact_id
        ))

        connection.commit()

        print(f"Email log saved for {name}")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    send_daily_emails()