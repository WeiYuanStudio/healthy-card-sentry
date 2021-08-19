import requests
from bs4 import BeautifulSoup


class Secure:
    _WORK_JLUZH_DOMAIN = 'https://work.zcst.edu.cn/'  # 任意选取CAS的一个服务作为登录
    _JLUZH_CAS_DOMAIN = 'https://authserver.zcst.edu.cn/cas/login'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, session):
        """使当前会话通过CAS登录，之后所有通过CAS认证的服务都将会自动认证"""
        execution = self.get_execution(self._WORK_JLUZH_DOMAIN)

        session.post(self._JLUZH_CAS_DOMAIN, data={
            "username": self.username,
            "password": self.password,
            "execution": execution,
            "_eventId": "submit",
            "loginType": 1,
            "submit": "登 录",
        }, headers={
            "Referer": self._JLUZH_CAS_DOMAIN,
            "Origin": "https://authserver.zcst.edu.cn",
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/47.0.2526.80 Safari/537.36',
            'Pragma': 'no-cache',
            'Cache-Control': 'max-age=0',
            'Host': "authserver.zcst.edu.cn",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
        })

    def get_execution(self, service):
        """获取CAS页面的execution字段"""
        r = requests.get(self._JLUZH_CAS_DOMAIN, params={
            "service": service
        })

        soup = BeautifulSoup(r.content, 'html.parser')
        elem = soup.find('input', attrs={"name": "execution"})

        return elem['value']
