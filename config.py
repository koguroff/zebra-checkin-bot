import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Configuration
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///checkin_bot.db')

# Working Hours Configuration
REGULAR_HOURS_PER_DAY = 8
WORK_START_HOUR = 9  # 9 AM
WORK_END_HOUR = 18   # 6 PM

# Admin Configuration
ADMIN_IDS = [int(id) for id in os.getenv('ADMIN_IDS', '').split(',') if id]

# Timezone Configuration
TIMEZONE = os.getenv('TIMEZONE', 'UTC')