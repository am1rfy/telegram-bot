from data import URL, generate_params, check_params, read_params
from re import sub
from requests import get
import json


def generate_email(url=URL) -> str:
    res = get(url, params=generate_params)
    mailbox = res.text
    return sub('[\[|"|\]]', '', mailbox)


def check_inbox(mailbox, url=URL) -> list:
    check_params['login'] = mailbox.partition('@')[0]
    check_params['domain'] = mailbox.partition('@')[2]

    res = get(url, params=check_params)
    return res.json()


def read_msg(mailbox, id, url=URL) -> str:
    read_params['login'] = mailbox.partition('@')[0]
    read_params['domain'] = mailbox.partition('@')[2]
    read_params['id'] = id

    res = get(url, params=read_params)
    res_text = res.text
    msg_content = json.loads(res_text)

    return msg_content['textBody']
