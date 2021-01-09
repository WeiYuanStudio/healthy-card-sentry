import requests
from bs4 import BeautifulSoup


class Secure:
    _MY_JLUZH_DOMAIN = 'https://my.jluzh.edu.cn/_web/fusionportal/index.jsp?_p=YXM9MSZwPTEmbT1OJg__'  # 参数p未知
    _JLUZH_CAS_DOMAIN = 'https://authserver.jluzh.edu.cn/cas/login'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login_my(self, session):
        """登录我的吉珠"""
        execution = self.get_execution(self._MY_JLUZH_DOMAIN)
        r = requests.post(self._JLUZH_CAS_DOMAIN, data={
            "username": self.username,
            "password": self.password,
            "execution": execution,
            "_eventId": "submit",
            "loginType": 1,
            "submit": "登 录",
        }, headers={
            "Referer": self._JLUZH_CAS_DOMAIN,
            "Origin": "https://authserver.jluzh.edu.cn",
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/47.0.2526.80 Safari/537.36',
            'Pragma': 'no-cache',
            'Cache-Control': 'max-age=0',
            'Host': "authserver.jluzh.edu.cn",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
        }, allow_redirects=False)

        url_with_ticket = r.headers['Location']  # 目标平台带ticket参数地址

        print(url_with_ticket)

        target_cookie = session.get(url_with_ticket, headers={
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/47.0.2526.80 Safari/537.36'
        }).headers['Set-Cookie']  # 通过登录目标平台，获取Cookie

        return target_cookie

    def get_execution(self, service):
        """获取CAS页面的execution字段"""
        r = requests.get(self._JLUZH_CAS_DOMAIN, params={
            "service": service
        })

        soup = BeautifulSoup(r.content, 'html.parser')
        elem = soup.find('input', attrs={"name": "execution"})

        return elem['value']
