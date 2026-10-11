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

def edit_event(parameter_to_edit):
    event_id = input("What event you like to edit?")
    parameter_to_edit = input("What parameter would you like to edit?")
    new_parameter = input("Enter new value:")
    match(parameter_to_edit):
        case "title": cur.execute("UPDATE events SET title =%s WHERE id = %s", (new_parameter, event_id,))
        case "description": cur.execute("UPDATE events SET description =%s WHERE id = %s", (new_parameter, event_id,))
        case "start_time": cur.execute("UPDATE events SET start_time =%s WHERE id = %s", (new_parameter, event_id,))
        case "remind_before": cur.execute("UPDATE events SET remind_before =%s WHERE id = %s", (new_parameter, event_id,))
        case "is_recurring": cur.execute("UPDATE events SET is_recurring =%s WHERE id = %s", (new_parameter, event_id,))
        case _: return("Unknown parameter")
    conn.commit()
    return "Event updated successfully"


start_time = datetime(2026,9,21,17,30)

#edit_event()
#print(select())
#cur.close()