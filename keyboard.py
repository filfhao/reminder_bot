from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

get_events_text = "📆 My events"
get_uni_schedule_text = "🎓 University schedule"
get_contact_text = "✉️ Contact"

main_keyboard = ReplyKeyboardMarkup(
    [
        [get_events_text, get_uni_schedule_text],
        [get_contact_text]
    ], resize_keyboard=True
)

inline_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("➕ Add event", callback_data = "add_event"),
        InlineKeyboardButton("✏️ Edit event", callback_data="edit_event"),
        InlineKeyboardButton("🗑️ Delete event", callback_data="delete_event")

    ]
])

recurrence_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("❌ No ", callback_data="recurrence_none"),
        InlineKeyboardButton("📅 Every day", callback_data="recurrence_day")
    ],
    [
        InlineKeyboardButton("📅 Every week", callback_data="recurrence_week"),
        InlineKeyboardButton("📅 Every month", callback_data="recurrence_month")
    ]
])


remind_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🔕 No reminder", callback_data="remind_none"),
        InlineKeyboardButton("15 minutes", callback_data="remind_15")
    ],
    [
        InlineKeyboardButton("30 minutes", callback_data="remind_30"),
        InlineKeyboardButton("1 hour", callback_data="remind_60")
    ]
])


edit_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Title", callback_data="edit_title"),
        InlineKeyboardButton("Description", callback_data="edit_description")
    ],
    [
        InlineKeyboardButton("Start time", callback_data="edit_start_time"),
        InlineKeyboardButton("End time", callback_data="edit_end_time")
    ],
    [
        InlineKeyboardButton("Recurrence", callback_data="edit_recurrence"),
        InlineKeyboardButton("Reminder", callback_data="edit_remind")
    ]
])


