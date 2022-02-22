import telebot
from config import token

bot = telebot.TeleBot(token)

if __name__ == '__main__':
    bot.infinity_polling()
