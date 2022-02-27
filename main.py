from telebot import TeleBot, types
from config import TOKEN
from interaction import generate_email, check_inbox, read_msg

bot = TeleBot(TOKEN)
# адрес временной почты
mailbox: str = None
# список с информацией о сообщениях
msgs_list: list = None


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.from_user.id,
                     f'Привет, {message.from_user.username}!')


def waiting(message):
    bot.send_message(message.from_user.id, 'Жду...')


@bot.message_handler(commands=['new_mail'])
def get_mailbox(message):
    global mailbox
    mailbox = generate_email()
    bot.send_message(message.from_user.id, f'Ваша временная почта: {mailbox}')


@bot.message_handler(commands=['get_messages_list'])
def get_list_msgs(message):
    global mailbox
    global msgs_list

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if mailbox != None:
        msgs_list = check_inbox(mailbox)

        if len(msgs_list) != 0:
            for i in range(len(msgs_list)):
                id_markup = types.KeyboardButton(text=msgs_list[i]['id'])
                markup.add(id_markup)

                msg_format = f'ID: {msgs_list[i]["id"]}\n' + \
                    f'От кого: {msgs_list[i]["from"]}\n' + \
                    f'Тема: {msgs_list[i]["subject"]}\n' + \
                    f'Дата и время: {msgs_list[i]["date"]}'

                msg = bot.send_message(message.from_user.id, text=f'{msg_format}\nВведите ID сообщения для прочтения',
                                       reply_markup=markup)

                bot.register_next_step_handler(msg, get_msg_content)
        else:
            bot.send_message(message.from_user.id, 'Ящик пуст')
    else:
        bot.send_message(message.from_user.id,
                         'Сначала получите временную почту командой /new_mail')


@bot.message_handler(commands=['read_message'], content_types=['text'])
def get_msg_content(message):
    global mailbox
    global msgs_list

    if mailbox != None:
        if msgs_list != None:
            content = read_msg(mailbox, message.text)
            res = f'{content}'
            step = waiting
        else:
            res = 'Сначала получите список сообщений командой /get_messages_list'
            step = get_list_msgs
    else:
        res = 'Сначала получите временную почту командой /new_mail'
        step = get_mailbox

    msg = bot.send_message(message.from_user.id, text=res)
    bot.register_next_step_handler(msg, step)


bot.polling(non_stop=True, interval=0)
