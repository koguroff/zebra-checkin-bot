from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from database.database import get_db
from database.models import User, CheckIn

async def check_in(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = next(get_db())
    
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        user = User(telegram_id=user_id, username=update.effective_user.username)
        db.add(user)
        db.commit()
    
    # Check if there's an open check-in
    open_checkin = db.query(CheckIn).filter(
        CheckIn.user_id == user.id,
        CheckIn.check_out_time == None
    ).first()
    
    if open_checkin:
        await update.message.reply_text("You already have an active check-in!")
        return
    
    new_checkin = CheckIn(
        user_id=user.id,
        check_in_time=datetime.now()
    )
    db.add(new_checkin)
    db.commit()
    
    await update.message.reply_text("✅ Successfully checked in!")

async def check_out(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = next(get_db())
    
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        await update.message.reply_text("You need to check in first!")
        return
    
    open_checkin = db.query(CheckIn).filter(
        CheckIn.user_id == user.id,
        CheckIn.check_out_time == None
    ).first()
    
    if not open_checkin:
        await update.message.reply_text("You need to check in first!")
        return
    
    checkout_time = datetime.now()
    open_checkin.check_out_time = checkout_time
    
    # Calculate hours worked
    time_diff = checkout_time - open_checkin.check_in_time
    hours_worked = time_diff.total_seconds() / 3600
    open_checkin.total_hours = round(hours_worked, 2)
    
    db.commit()
    
    await update.message.reply_text(f"✅ Successfully checked out!\nHours worked: {hours_worked:.2f}")