from data import URL, generate_params, check_params, read_params
from re import sub
from requests import get
import json


def generate_email(url=URL) -> str:
    res = get(url, params=generate_params)
    if res:
        mailbox = res.text
        return sub('[\[|"|\]]', '', mailbox)
    else:
        return 'Failed to receive mail. Responce error'


def check_inbox(mailbox, url=URL) -> list or str:
    check_params['login'] = mailbox.partition('@')[0]
    check_params['domain'] = mailbox.partition('@')[2]

    res = get(url, params=check_params)

    if res:
        return res.json()
    else:
        return 'Failed to get message list. Responce error'


def read_msg(mailbox, id, url=URL) -> str:
    read_params['login'] = mailbox.partition('@')[0]
    read_params['domain'] = mailbox.partition('@')[2]
    read_params['id'] = id

    res = get(url, params=read_params)

    if res:
        res_text = res.text
        try:
            msg_content = json.loads(res_text)
            return msg_content['textBody']
        except json.JSONDecodeError:
            return 'There is no message with this id'
    else:
        return 'Failed to read message. Responce error'
