from telegram import Update

import psycopg
from dotenv import load_dotenv
import os
from datetime import datetime
from pprint import pprint

load_dotenv()

conn = psycopg.connect(
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT"),
    dbname = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD")
)
if conn:
    print("Connected!")

cur = conn.cursor()


# def select():
#     cur.execute("SELECT * FROM events")
#     return cur.fetchall()

def select(user_tg_id):
    cur.execute("SELECT * FROM events WHERE user_id = %s", (user_tg_id,))
    list = cur.fetchall()
    if not list:
        result = "You have no events yet"
    else:
        result = ""
        for i in list:
            result += f"Event id: {i[0]}\n"
            result += f"Title: {i[2]}\n"
            result += f"Description: {i[3]}\n"
            result += f"Start time: {i[4]}\n"
            result += f"Remind before: {i[5]}\n"
            result += f"Is recurring: {i[6]}\n"

            result += "-"*20 + "\n"
    return result

def event_exists(user_id, title, exlude_event_id = None):
    cur.execute("SELECT 1 FROM events WHERE user_id = %s AND title = %s AND id IS DISTINCT FROM %s",(user_id,title, exlude_event_id,))
    return cur.fetchone() is not None

def get_event(user_tg_id, event_id):
    cur.execute("SELECT * FROM events WHERE user_id = %s and id =%s", (user_tg_id,event_id,))
    event = cur.fetchone()
    if event is None:
        return None

    result = ""

    result += f"Event id: {event[0]}\n"
    result += f"Title: {event[2]}\n"
    result += f"Description: {event[3]}\n"
    result += f"Start time: {event[4]}\n"
    result += f"Remind before: {event[5]}\n"
    result += f"Is recurring: {event[6]}\n"

    return result


def add_event(user_id, title, start_time, description = None, end_time=None, remind_before=None,
              is_recurring=False, recurrence=None):
    cur.execute("INSERT INTO events(user_id, title, start_time, description, end_time, remind_before,"
              "is_recurring, recurrence) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (user_id, title, start_time,description, end_time, remind_before,is_recurring, recurrence))
    conn.commit()

def delete_event(id):
    cur.execute("DELETE FROM events WHERE id = %s", (id,))
    conn.commit()

def edit_event(user_id, event_id, parameter_to_edit, new_value):
    allowed_parameters = {"title", "description", "start_time", "end_time", "remind_before", "is_recurring"}
    if parameter_to_edit not in allowed_parameters:
        return False
    cur.execute(f"UPDATE events SET {parameter_to_edit} =%s WHERE user_id = %s AND id = %s", (new_value, user_id, event_id,))
    conn.commit()

start_time = datetime(2026,9,21,17,30)

#edit_event()
#print(select())
#cur.close()