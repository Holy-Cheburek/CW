import logging # Imports the logging module for logging events.
import random
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent # Imports necessary classes from the telegram library.
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler # Imports necessary classes from the telegram.ext library.
from uuid import uuid4 # Imports the uuid module for generating unique IDs.

# Sets up basic logging configuration.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # Defines the format for log messages.
    level=logging.INFO # Sets the logging level to INFO, meaning INFO and higher level messages will be logged.
)

# Defines the function for the /start command.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message( # Sends a message through the bot.
        chat_id=update.effective_chat.id, # Gets the chat ID from where the command was sent.
        text='''Hello! My name is Yapper! I am a universal bot who can do different things! 
I can echo anything that isn't a command, but I prefer YELLING! Add '/caps' before a text you want me to yell! 
Or mention me with @Yapper_Python_bot to caps your text in other chats!
I can also periodically send motivational messages! Type '/motivate' if you need some!'''  # Sets the text of the message.
    )

# Defines the function for echoing back text messages.
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message( # Sends a message through the bot.
        chat_id=update.effective_chat.id, # Gets the chat ID from where the message was sent.
        text=update.message.text # Gets the text content of the received message and sets it as the text to be sent.
    )

# Defines the function for the /caps command.
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper() # Joins the command's arguments with spaces and converts them to uppercase.
    await context.bot.send_message( # Sends a message through the bot.
        chat_id=update.effective_chat.id, # Gets the chat ID from where the command was sent.
        text=text_caps # Sets the text of the message to the uppercased text.
    )

# Defines the function for inline queries.
async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query # Gets the user's query from the inline query.
    if not query: # Checks if the query is empty.
        return # If the query is empty, return and do nothing.
    results = [] # Initializes an empty list to store the results of the inline query.
    results.append( # Adds an InlineQueryResultArticle to the results list.
        InlineQueryResultArticle(
            id=str(uuid4()), # Generates a unique ID for this result.
            title='Caps', # Sets the title of the result.
            input_message_content=InputTextMessageContent(query.upper()) # Sets the content of the message to be sent when the result is selected (uppercased query).
        )
    )
    await context.bot.answer_inline_query( # Sends the results back to the user.
        update.inline_query.id, results # Uses the inline query ID and the results.
        )

# Defines the function for handling unknown commands.
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message( # Sends a message through the bot.
        chat_id=update.effective_chat.id, # Gets the chat ID from where the command was sent.
        text="Sorry, I didn't understand that command." # Sets the text of the message.
    )

async def callback_motivate(context: ContextTypes.DEFAULT_TYPE):
  #Sends a randomly chosen reminder message to the chat.
    reminders = [
      f"Remember, {context.job.data}! Failure isn't the opposite of success - it's part of it!",
      f"Hey {context.job.data}, don't forget that consistency is key!",
      f"{context.job.data}, a little progress each day adds up to big results!",
      f"Quick reminder for you, {context.job.data}! Keep your goals in mind.",
      f"{context.job.data}, if your dreams don't scare you, they are too small!"
    ]
    chosen_reminder = random.choice(reminders) 
    await context.bot.send_message(chat_id=context.job.chat_id, text=chosen_reminder)
   
 
 
async def callback_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name
    await context.bot.send_message(chat_id=chat_id, text='Motivational mode activated!')
    # Begin looping motivational message
    job_repeat = context.job_queue.run_repeating(callback_motivate, first = 1, interval=20, last = 62, data=name, chat_id=chat_id) #Will send 4 messages across 1 minute and stop


if __name__ == '__main__': # Checks if the script is being run directly.
    application = ApplicationBuilder().token('TOKEN').build() # Creates an application object with the bot's token.

    start_handler = CommandHandler('start', start) # Creates a handler for the /start command, linking it to the start function.
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo) # Creates a handler for all text messages that are not commands, linking it to the echo function.
    caps_handler = CommandHandler('caps', caps) # Creates a handler for the /caps command, linking it to the caps function.
    inline_caps_handler = InlineQueryHandler(inline_caps) # Creates a handler for inline queries, linking it to the inline_caps function.
    timer_handler = CommandHandler('motivate', callback_timer)
    unknown_handler = MessageHandler(filters.COMMAND, unknown) # Creates a handler for all unknown commands, linking it to the unknown function.

    application.add_handler(start_handler) # Adds the start handler to the application.
    application.add_handler(echo_handler) # Adds the echo handler to the application.
    application.add_handler(caps_handler) # Adds the caps handler to the application.
    application.add_handler(inline_caps_handler) # Adds the inline caps handler to the application.
    application.add_handler(timer_handler) # Adds the motivational messages handler.
    application.add_handler(unknown_handler) # Adds the unknown handler to the application.
    application.run_polling() # Starts the bot and starts listening for updates.
