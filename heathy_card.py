
class Card:
    _HEALTHY_CARD_PRSET_DICT_PATH = 'https://work.jluzh.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.work.jlzh.jkxxtb.jkxxcj.queryEmp.biz.ext'

    def __init__(self, session):
        r = session.post(self._HEALTHY_CARD_PRSET_DICT_PATH, headers={
            'referer': 'https://work.jluzh.edu.cn/default/work/jlzh/jkxxtb/jkxxcj.jsp'
        })

        print(r.content.decode(encoding='utf-8'))
