from requests import Session

class ModSession(Session):
    def get(self, url, **kwargs):
        kwargs.setdefault('allow_redirects', True)

        if url.find('work.zcst.edu.cn'):
            headers = {'referer': 'https://work.zcst.edu.cn/'}
            kwargs.setdefault('headers', headers)
        return self.request('GET', url, **kwargs)
