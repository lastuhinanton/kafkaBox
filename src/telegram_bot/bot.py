from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from telegram.ext.filters import TEXT, Command
from confluent_kafka import Producer
import random


GLOBAL_VARIABLE = str()

# kafka configuration
kafka_config = {
  'bootstrap.servers': 'node1:9092,node2:9092,node3:9092',
  'client.id': 'kafka-telegram-bot',
  'acks': 'all'
}

producer = Producer(kafka_config)

def delivery_report(err, msg):
  global GLOBAL_VARIABLE
  """Callback function to confirm message delivery."""
  if err is not None:
    GLOBAL_VARIABLE = f"Message delivery failed: {err}"
  else:
    GLOBAL_VARIABLE = f"Message delivered to {msg.topic()} [partition: {msg.partition()} offset: {msg.offset()}]"

# Command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text('Hello! I am your bot. How can I assist you today?')

# Handler for normal text messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  global GLOBAL_VARIABLE
  key_number = random.uniform(1.0, 10.0)

  try:
    producer.produce("TELEGRAMM_BOT", key=str(key_number), value=update.message.text, callback=delivery_report)
  except:
    print(f"Error producing message: {e}")

  producer.flush()
  #await update.message.reply_text(GLOBAL_VARIABLE)
  await update.message.reply_text(f'You said: {update.message.text}\n\n{GLOBAL_VARIABLE}')

def main():
  application = Application.builder().token("7412531742:AAEKK0uhxPuMfUDjcw2Vpszydfexri9CfWs").build()

  # Add command handler for /start
  application.add_handler(CommandHandler("start", start))
 
  # Add message handler for regular text messages
  application.add_handler(MessageHandler(TEXT & ~Command(), echo))
  
  # Start the Bot
  application.run_polling()

if __name__ == '__main__':
    main()
