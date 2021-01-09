import os
from requests import Session

from secure import Secure
from heathy_card import Card


def main_handler(event, context):
    """云函数入口"""
    username = os.environ.get('username')
    password = os.environ.get('password')

    with Session() as session:
        session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)'}  # 设置UA避免被防火墙拦截

        Secure(username, password).login(session)

        card = Card(session)
        card.submit()


if __name__ == '__main__':
    """本地调试"""
    main_handler(None, None)
