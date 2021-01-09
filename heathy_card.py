import json
from datetime import datetime


class Card:
    _HEALTHY_CARD_PRESET_DICT_PATH = 'https://work.jluzh.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.work.jlzh.jkxxtb.jkxxcj.queryEmp.biz.ext'

    def __init__(self, session):
        r = session.post(self._HEALTHY_CARD_PRESET_DICT_PATH, headers={
            'referer': 'https://work.jluzh.edu.cn/default/work/jlzh/jkxxtb/jkxxcj.jsp'
        })

        resp_dict = json.loads(r.content.decode(encoding='utf-8'))
        print(resp_dict)

        self._CLASS_NAME = resp_dict['result']['bjmc']  # 班级名称 '计算机学院xxxx级xx班'
        self._COUNSELOR_ID = resp_dict['result']['fdygh']  # 辅导员工号
        self._COUNSELOR_NAME = resp_dict['result']['fdymc']  # 辅导员名称
        self._STUDENT_PHONE = resp_dict['result']['lxdh']  # 学生联系电话
        self._STUDENT_GRADE = resp_dict['result']['nj']  # 学生入学学年 第xxxx届学生
        self._USER_TYPE = resp_dict['result']['qq']  # 人员身份? 2
        self._DORM_ID = resp_dict['result']['ssh']  # 宿舍号 '榕x-xxx-x'
        self._GENDER = resp_dict['result']['xb']  # 性别ID: 男 1 | 女 2
        self._MAJOR = resp_dict['result']['zymc']  # 专业名称 '软件工程'

        self._LOCATION_TYPE = '2'  # 所在地区: 珠海1 | 在广东2 | 其他地区4

        self.get_user_info(session)

    def submit(self):
        post_dict = {
            'sqrid': self._USER_ID,
            'sqbmid': self._ORG_ID,
            'fdygh': self._COUNSELOR_ID,
            'rysf': self._USER_TYPE,
            'bt': f'{self._get_fmt_date()} {self._USER_REAL_NAME} 健康卡填报',  # 标题
            'sqrmc': self._USER_REAL_NAME,
            "gh": self._USER_STUDENT_ID,
            "xb": self._GENDER,
            "sqbmmc": self._ORG_NAME,
            "nj": self._STUDENT_GRADE,
            "zymc": self._MAJOR,
            "bjmc": self._CLASS_NAME,
            "fdymc": self._COUNSELOR_NAME,
            "ssh": self._DORM_ID,
            "lxdh": self._STUDENT_PHONE,
            "tbrq": self._get_fmt_date(),
            "tjsj": self._get_fmt_date_time(),
            "xjzdz": "广东xx市xx县",  # 常住地址
            "jqqx": "广东xx",  # 假期期间去向

            # 健康设定
            "sfqwhb": "否",  # 去往湖北
            "sfjchbjry": "否",
            "sfjwhy": "否",
            "sfjwhygjdq": "",
            "xrywz": self._LOCATION_TYPE,
            "jtdz": "在校",  # 具体地址
            "grjkzk": "1",  # 健康码
            "jrtw": "36",  # 体温
            "qsjkzk": "1",  # 亲属状况
            "jkqk": "1",  # 其他症状
            "cn": [
                "本人承诺登记后、到校前不再前往其他地区"
            ],  # 承诺
            "bz": "", # 备注
            "_ext": "{}",
            "__type": "sdo:com.sudytech.work.jlzh.jkxxtb.jkxxcj.TJlzhJkxxtb"
        }

        print({'entity': post_dict})

        # 如果今天填过健康卡，附带一个实体ID，更新实体
        if True:
            post_dict['id'] = -1

    def get_user_info(self, session):
        r = session.get(
            'https://work.jluzh.edu.cn/default/base/workflow/com.sudytech.work.jluzh_LoginUser.jluzhLogin.LoginUser.jluzhUtil.biz.ext')
        resp_dict = json.loads(r.content.decode(encoding='utf-8'))
        print(resp_dict)

        self._USER_ID = str(resp_dict['result']['EMPID'])  # 用户ID
        self._ORG_ID = str(resp_dict['result']['ORGID'])  # 应该是学院ID
        self._ORG_NAME = resp_dict['result']['ORGNAME']  # 学院名称
        self._USER_REAL_NAME = resp_dict['result']['EMPNAME']  # 用户真实姓名
        self._USER_STUDENT_ID = resp_dict['result']['EMPCODE']  # 用户学号

    @staticmethod
    def _get_fmt_date():
        now = datetime.now()
        return now.strftime("%Y-%m-%d")

    @staticmethod
    def _get_fmt_date_time():
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M")
