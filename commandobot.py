import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler,MessageHandler, filters
from dotenv import load_dotenv

# DOCS
# https://docs.python-telegram-bot.org/en/v21.6/index.html

load_dotenv()
api_key = os.getenv("API_KEY")

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

logo = "Commando News 🎗"

# Define the command handler for /start
async def start(update: Update, context) -> None:
    """Send a message when the command /start is issued."""
    logger.info(f"User '[{update.effective_user.id}] - {update.effective_user.full_name}'  started the bot.")
    await update.message.reply_text('Hello Tembel!')

# Define the message handler to detect if sender is admin and edit the message to add Logo
async def detect_report(update: Update, context) -> None:
    """Detect if the sender is an admin, and if so, edit their message by adding Logo."""
    # Get the chat ID and user ID
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    message_id = update.message.message_id

    # Fetch the chat member (the user who sent the message)
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    logger.info(chat_member)

    # Check if the user is an admin (status could be 'administrator' or 'creator')  
    if chat_member.user.username in ['GroupAnonymousBot'] and logo not in update.message.text:
        # User is an admin, so edit the message by adding Logo
        new_text = f"<strong>{update.message.text}\n{logo}</strong>"

        # Delete the original message
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

        # Send the new message anonymously (if bot is set as anonymous admin)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=new_text, parse_mode='HTML')

        logger.info(f"Anonymous message sent by bot in place of admin {user_id}.")

    else:
        # Log if the user is not an admin
        logger.info(f"User {user_id} is not an admin and cannot have their message edited.")

# Main function to set up the bot
def main():
    """Start the bot."""
    # Create the Application and pass your bot's token.
    application = Application.builder().token(api_key).build()

    # Add the command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Add the message handler to detect Commando News Reports and add Logo
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_report))

    # Run the bot until manually stopped
    logger.info("Bot is starting...")
    application.run_polling()  # This will start the polling loop automatically

# If running as the main module, start the bot
if __name__ == '__main__':
    main()
