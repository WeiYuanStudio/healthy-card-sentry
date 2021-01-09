import os
from requests import Session

from secure import Secure
from heathy_card import Card

def main_handler(event, context):
    """云函数入口"""
    username = os.environ.get('username')
    password = os.environ.get('password')

    with Session() as session:
        session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)'}

        Secure(username, password).login_my(session)
        r = session.get('https://my.jluzh.edu.cn/_web/fusionportal/index.jsp?_p=YXM9MSZwPTEmbT1OJg__')
        # print(r.content.decode(encoding='utf-8'))
        # card = Card(session)






        r = session.get('https://my.jluzh.edu.cn/_web/fusionportal/index.jsp?_p=YXM9MSZwPTEmbT1OJg__')

if __name__ == '__main__':
    """本地调试"""
    main_handler(None, None)
