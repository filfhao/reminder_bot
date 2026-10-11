from telegram import Update
from config import BOT_USERNAME
from telegram.ext import ContextTypes
from responses import handle_response
from db_connection import select, add_event,edit_event,delete_event
from keyboard import main_keyboard, get_events_text, get_uni_schedule_text, get_contact_text, inline_keyboard, recurrence_keyboard,remind_keyboard
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo


#Commands
async def start_command(update, context):
    await update.message.reply_text(
        "👋 Hello! Nice to meet you!\n\n"
        "What would you like to do?",
        reply_markup = main_keyboard
    )



async def help_command(update, context):
    await update.message.reply_text(
        "Hey! 👋 Here's what I can do:\n\n"
        "🌤 Weather — get the current weather in any city\n"
        "💱 Currency — check exchange rates\n"
        "✉️ Contact the owner — get in touch with me\n\n"
        "Just choose an option from the keyboard below! 😊")

def parse_datetime(text):
    try:
        return datetime.strptime(
            text,
            "%d.%m.%Y %H:%M"
        ).replace(tzinfo=ZoneInfo("Europe/Kyiv"))
    except ValueError:
        return None

def parse_end_time(text, start_time):
    try:
        end_time = datetime.strptime(
            text,
            "%H:%M"
        ).time()

        return datetime.combine(
            start_time.date(),
            end_time
        ).replace(tzinfo=ZoneInfo("Europe/Kyiv"))

    except ValueError:
        return None

#Responses
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if context.user_data.get("step") == "title":
        title = text

        context.user_data["title"] = title
        context.user_data["step"] = "description"

        await update.message.reply_text("Enter the description: \n If there is no description enter \"-\"")
        return

    if context.user_data.get("step") == "description":
        if text == "-":
            description = None
        else:
            description = text
        context.user_data["description"] = description

        context.user_data["step"] = "start_time"

        await update.message.reply_text("Enter the start date and time:\n\nFormat: 03.10.2026 09:00")
        return

    if context.user_data.get("step") == "start_time":
        start_time = parse_datetime(text)

        if start_time is None:
            await update.message.reply_text(
                "❌ Invalid format.\n"
                "Please enter the date and time like this:\n"
                "03.10.2026 09:00"
            )
            return
        context.user_data["start_time"] = start_time

        context.user_data["step"] = "end_time"

        await update.message.reply_text("🕐 When does the event end?\n"
            "For example: 18:30\n"
            "If there is no end time, enter \"-\"")
        return

    if context.user_data.get("step") == "end_time":
        start_time = context.user_data["start_time"]
        if text == "-":
            end_time = None
        else:
            start_time = context.user_data["start_time"]
            end_time = parse_end_time(text, start_time)

            if end_time is None:
                await update.message.reply_text(
                    "❌ Invalid time.\n"
                    "Please enter the time like this: 18:30"
                )
                return

            if end_time <= start_time:
                await update.message.reply_text(
                    "❌ The end time must be later than the start time."
                )
                return
        context.user_data["end_time"] = end_time
        if end_time:
            time_text = (f"🕐 {start_time.strftime('%H:%M')}"
                        f"–{end_time.strftime('%H:%M')}\n\n")
        else:
            time_text = (f"🕐 {start_time.strftime('%H:%M')}")
        await update.message.reply_text(
            "🔁 Would you like this event to repeat?\n"
                f"📅 {start_time.strftime('%d.%m.%Y')}\n"
                f"{time_text}",
                reply_markup=recurrence_keyboard
            )
        return

    if text == get_events_text:
        user_tg_id = update.effective_user.id
        events = select(user_tg_id)
        await update.message.reply_text(events, reply_markup=inline_keyboard)
        return

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print("Bot:", response)
    await update.message.reply_text(response)

async def finish_event(update, context):
    query = update.callback_query

    user_tg_id = query.message.chat.id

    title = context.user_data["title"]
    description = context.user_data["description"]
    start_time = context.user_data["start_time"]
    end_time = context.user_data["end_time"]
    is_recurring = context.user_data["is_recurring"]
    recurrence = context.user_data["recurrence"]
    remind_before = context.user_data["remind_before"]

    add_event(
        user_id=user_tg_id,
        title=title,
        description=description,
        start_time=start_time,
        end_time=end_time,
        remind_before=remind_before,
        is_recurring=is_recurring,
        recurrence=recurrence
    )

    context.user_data.clear()

    await query.message.reply_text("✅ Event added!", reply_markup = main_keyboard)

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "add_event":
        context.user_data["step"] = "title"
        await query.edit_message_text("Enter the event title:")
    elif query.data == "edit_event":
        await query.edit_message_text("You choosed an edit event button")
    elif query.data == "delete_event":
        await query.edit_message_text("You choosed an delete event button")

    elif query.data == "recurrence_none":
        context.user_data["is_recurring"] = False
        context.user_data["recurrence"] = None
        context.user_data["step"] = "remind_before"
        await query.edit_message_text(
            "⏰ When should I remind you?",
            reply_markup=remind_keyboard
        )

    elif query.data == "recurrence_day":
        context.user_data["is_recurring"] = True
        context.user_data["recurrence"] = "day"
        context.user_data["step"] = "remind_before"
        await query.edit_message_text(
            "⏰ When should I remind you?",
            reply_markup=remind_keyboard
        )

    elif query.data == "recurrence_week":
        context.user_data["is_recurring"] = True
        context.user_data["recurrence"] = "week"
        context.user_data["step"] = "remind_before"
        await query.edit_message_text(
            "⏰ When should I remind you?",
            reply_markup=remind_keyboard
        )

    elif query.data == "recurrence_month":
        context.user_data["is_recurring"] = True
        context.user_data["recurrence"] = "month"
        context.user_data["step"] = "remind_before"
        await query.edit_message_text(
            "⏰ When should I remind you?",
            reply_markup=remind_keyboard
        )
    elif query.data == "remind_none":
        context.user_data["remind_before"] = None
        await finish_event(update, context)

    elif query.data == "remind_15":
        context.user_data["remind_before"] = 15
        await finish_event(update, context)

    elif query.data == "remind_30":
        context.user_data["remind_before"] = 30
        await finish_event(update, context)

    elif query.data == "remind_60":
        context.user_data["remind_before"] = 60
        await finish_event(update, context)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
