from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN
from handlers import start_command, help_command, handle_message, error


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()


    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))



    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    #Polling
    print('Polling...')
    app.run_polling(poll_interval=1)