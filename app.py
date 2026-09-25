import os
from datetime import date, timedelta

from dotenv import load_dotenv
from mssql_python import connect

from email_service import send_good_morning_email

from apscheduler.schedulers.blocking import BlockingScheduler

load_dotenv()

def send_daily_emails():

    connection_string = (
        f"Server={os.getenv('DB_SERVER')};"
        f"Database={os.getenv('DB_NAME')};"
        f"UID={os.getenv("DB_USER")};"
        f"PWD={os.getenv("DB_PASSWORD")};"
        "Encrypt=no;"
    )

    connection = connect(connection_string)
    cursor = connection.cursor()

    print("Database successfully connected!")

    today = date.today()

    cursor.execute("""
        SELECT Id, Name, Email, StartDate, IsActive
        FROM Contacts
    """)

    contacts = cursor.fetchall()

    for contact in contacts:
        contact_id = contact[0]
        name = contact[1]
        email = contact[2]
        start_date = contact[3]
        is_active = contact[4]

        end_date = start_date + timedelta(days=2)

        if not is_active:
            continue
        if not (start_date <= today <= end_date):
            continue

        cursor.execute("""
            SELECT COUNT(*)
            FROM EmailLogs
            WHERE ContactId = ?
            AND SentDate = ?    
    """, (contact_id, today))

        log_count = cursor.fetchone()[0]

        if log_count > 0:
            print(f"Email already sent to {name} today.")
            continue

        send_good_morning_email(name, email)

        cursor.execute("""
            INSERT INTO EmailLogs (ContactId, SentDate)
            VALUES(?, ?)
    """, (contact_id, today))

        connection.commit()

        print(f"Email log saved for {name}")

    cursor.close()
    connection.close()

scheduler = BlockingScheduler(
    timezone="Asia/Kolkata"
)

scheduler.add_job(
    send_daily_emails,
    "cron",
    hour=6,
    minute=0
)

print("Scheduler started. Waiting for 6:00 AM.")

scheduler.start()