from telebot import TeleBot, types
from config import TOKEN
from interaction import generate_email, check_inbox, read_msg

# cам бот
bot = TeleBot(TOKEN)
# адрес временной почты
mailbox: str = None
# список с информацией о сообщениях
msgs_list: list = None


def create_markup(*args):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(args)):
        markup.add(types.KeyboardButton(text=args[i]))
    return markup


@ bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.from_user.id,
                     text=f'Hello, {message.from_user.username}',
                     reply_markup=create_markup('/new_mail', '/get_messages_list', '/read_message'))


def waiting(message):
    bot.send_message(message.from_user.id,
                     text='Waiting...',
                     reply_markup=create_markup('/new_mail', '/get_messages_list', '/read_message'))


@ bot.message_handler(commands=['new_mail'])
def get_mailbox(message):
    global mailbox
    mailbox = generate_email()
    bot.send_message(message.from_user.id, f'Your temporary mail: {mailbox}')


@ bot.message_handler(commands=['get_messages_list'])
def get_list_msgs(message):
    global mailbox
    global msgs_list

    markup = create_markup()

    if mailbox != None:
        msgs_list = check_inbox(mailbox)

        if len(msgs_list) != 0:
            for i in range(len(msgs_list)):
                id_markup = types.KeyboardButton(text=msgs_list[i]['id'])
                markup.add(id_markup)

                msg_format = f'ID: {msgs_list[i]["id"]}\n' + \
                    f'From who: {msgs_list[i]["from"]}\n' + \
                    f'Subject: {msgs_list[i]["subject"]}\n' + \
                    f'Date: {msgs_list[i]["date"]}'

                msg = bot.send_message(message.from_user.id, text=f'{msg_format}\Enter the message id to read it',
                                       reply_markup=markup)

                bot.register_next_step_handler(msg, get_msg_content)
        else:
            bot.send_message(message.from_user.id, 'Mailbox is empty')
    else:
        bot.send_message(message.from_user.id,
                         'First you need to get the mail by command /new_mail')


@ bot.message_handler(commands=['read_message'], content_types=['text'])
def get_msg_content(message):
    global mailbox
    global msgs_list

    if mailbox != None:
        if len(msgs_list) != 0:
            content = read_msg(mailbox, message.text)
            res = f'{content}'
            step = waiting
        else:
            res = 'First you need to get messages list by command /get_messages_list'
            step = get_list_msgs
    else:
        res = 'First you need to get the mail by command /new_mail'
        step = get_mailbox

    msg = bot.send_message(message.from_user.id,
                           text=res,
                           reply_markup=create_markup('/new_mail', '/get_messages_list', '/read_message'))
    bot.register_next_step_handler(msg, step)


bot.polling(non_stop=True, interval=0)
