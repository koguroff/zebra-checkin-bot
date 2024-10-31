from telegram.ext import Application, CommandHandler
from handlers.user_handlers import check_in, check_out
from handlers.admin_handlers import get_overtime_report
from database.database import init_db
from config import TOKEN


def main():
    # Initialize database
    init_db()
    
    # Create application
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler('checkin', check_in))
    app.add_handler(CommandHandler('checkout', check_out))
    app.add_handler(CommandHandler('overtime', get_overtime_report))
    
    # Start bot
    print('Bot is running...')
    app.run_polling(poll_interval=1)

if __name__ == '__main__':
    main()