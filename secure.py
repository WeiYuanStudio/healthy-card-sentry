import requests
from bs4 import BeautifulSoup


class Secure:
    _MY_JLUZH_DOMAIN = 'https://my.jluzh.edu.cn/_web/fusionportal/index.jsp'
    _JLUZH_CAS_DOMAIN = 'https://authserver.jluzh.edu.cn/cas/login'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        print(self.get_execution())
        pass

    def get_execution(self):
        r = requests.get(self._JLUZH_CAS_DOMAIN, params={
            "service": self._MY_JLUZH_DOMAIN
        })

        soup = BeautifulSoup(r.content, 'html.parser')

        elem = soup.find('input', attrs={"name": "execution"})

        return elem['value']
