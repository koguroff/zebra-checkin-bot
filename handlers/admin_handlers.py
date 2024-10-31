from telegram import Update
from telegram.ext import ContextTypes
from database.database import get_db
from database.models import User, CheckIn
from datetime import datetime, timedelta
from config import ADMIN_IDS

async def is_admin(telegram_id: int) -> bool:
    return telegram_id in ADMIN_IDS

async def get_overtime_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = next(get_db())
    
    if not await is_admin(user_id):
        await update.message.reply_text("You don't have permission to use this command!")
        return
    
    # Parse the username from command arguments
    if not context.args:
        await update.message.reply_text("Please provide a username: /overtime @username")
        return
        
    username = context.args[0].replace("@", "")
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        await update.message.reply_text("User not found!")
        return
    
    # Calculate overtime (assuming 8 hours is regular time)
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    checkins = db.query(CheckIn).filter(
        CheckIn.user_id == user.id,
        CheckIn.check_in_time >= month_start
    ).all()
    
    total_hours = sum(checkin.total_hours or 0 for checkin in checkins)
    regular_hours = len(checkins) * 8
    overtime = max(0, total_hours - regular_hours)
    
    report = f"Overtime Report for @{username}\n"
    report += f"Total Hours: {total_hours:.2f}\n"
    report += f"Regular Hours: {regular_hours}\n"
    report += f"Overtime: {overtime:.2f} hours"
    
    await update.message.reply_text(report)