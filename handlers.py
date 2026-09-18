from telegram import Update
from config import BOT_USERNAME
from telegram.ext import ContextTypes
from responses import handle_response

#Commands
async def start_command(update, context):
    await update.message.reply_text(
        "👋 Hello! Nice to meet you!\n\n"
        "What would you like to do?")

async def help_command(update, context):
    await update.message.reply_text(
        "Hey! 👋 Here's what I can do:\n\n"
        "🌤 Weather — get the current weather in any city\n"
        "💱 Currency — check exchange rates\n"
        "✉️ Contact the owner — get in touch with me\n\n"
        "Just choose an option from the keyboard below! 😊")

#Responses
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print("i hear you!!!")
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

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

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
