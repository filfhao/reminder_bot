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

def select():
    cur.execute("SELECT * FROM events")
    result = cur.fetchall()
    for i in result:
        print("Event id:", i[0])
        print("Title:", i[2])
        print("Description:", i[3])
        print("Start time::", i[4])
        print("Remind before:", i[5])
        print("Is recurring:", i[6])

        print("-"*20)



def add_event(user_id, title, start_time):
    cur.execute("INSERT INTO events(user_id, title, start_time) VALUES (%s,%s,%s)", (user_id, title, start_time))
    conn.commit()

def delete_event(id):
    cur.execute("DELETE FROM events WHERE id = %s", (id,))
    conn.commit()

def edit_event():
    print(select())
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
select()
cur.close()