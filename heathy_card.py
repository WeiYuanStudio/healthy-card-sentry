import json
import os
from datetime import datetime, timezone, timedelta


class Card:
    _HEALTHY_CARD_PRESET_DICT_PATH = 'https://work.zcst.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.work.jlzh.jkxxtb.jkxxcj.queryEmp.biz.ext'
    _HEALTHY_CARD_POST_PATH = 'https://work.zcst.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.portalone.base.db.saveOrUpdate.biz.ext'
    _HEALTHY_CARD_QUERY_TODAY_PATH = 'https://work.zcst.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.work.jlzh.jkxxtb.jkxxcj.queryToday.biz.ext'

    def __init__(self, session):
        self._SESSION = session

        print('---- INIT USER INFO ----')
        self.get_user_info()  # 获取用户个人信息

        print('---- LOAD CARD PRESET ----')
        self._load_preset()  # 加载表单预设

    def _load_preset(self):
        r = self._SESSION.post(self._HEALTHY_CARD_PRESET_DICT_PATH)

        resp_dict = json.loads(r.content.decode(encoding='utf-8'))['result']

        print(resp_dict)

        self._CLASS_NAME = resp_dict.get('bjmc', None)  # 班级名称 '计算机学院xxxx级xx班'
        self._COUNSELOR_ID = resp_dict.get('fdygh', None)  # 辅导员工号
        self._COUNSELOR_NAME = resp_dict.get('fdymc', None)  # 辅导员名称
        self._STUDENT_PHONE = os.environ.get('PHONE') or resp_dict['lxdh']  # 学生联系电话
        self._STUDENT_GRADE = resp_dict.get('nj', None)  # 学生入学学年 第xxxx届学生
        self._USER_TYPE = resp_dict['qq']  # 人员身份? 2 学生 | 1 教师
        self._DORM_ID = resp_dict.get('ssh', None)  # 宿舍号 '榕x-xxx-x'
        self._GENDER = resp_dict['xb']  # 性别ID: 男 1 | 女 2
        self._MAJOR = resp_dict.get('zymc', None)  # 专业名称 '软件工程'

        self._LOCATION_TYPE = os.environ.get('LOCATION_TYPE') or '2'  # 所在地区: 珠海1 | 在广东2 | 其他地区4 Todo: 使用环境变量

    def submit(self):
        # 构建提交表单的参数
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
            "xjzdz": os.environ.get('LOCATION_DETAILED') or '广东省珠海市金湾区吉林大学珠海学院',  # 常住地址 Todo: 上移到init
            "jqqx": os.environ.get('LOCATION') or "广东省珠海市金湾区" if self._USER_TYPE != '1' else None,  # 假期期间去向，教师无该字段 Todo: 上移到init

            # 健康设定
            "sfqwhb": "否",  # 去往湖北
            "sfjchbjry": "否",
            "sfjwhy": "否",
            "sfjwhygjdq": "",
            "xrywz": self._LOCATION_TYPE,
            "jtdz": os.environ.get('LOCATION_DETAILED') or '广东省珠海市金湾区吉林大学珠海学院',  # 具体地址
            "grjkzk": "1",  # 健康码
            "jrtw": "36",  # 体温
            "qsjkzk": "1",  # 亲属状况
            "jkqk": "1",  # 其他症状
            "cn": [
                "本人承诺登记后、到校前不再前往其他地区"
            ],  # 承诺
            "bz": "无",  # 备注
            "_ext": "{}",
            "__type": "sdo:com.sudytech.work.jlzh.jkxxtb.jkxxcj.TJlzhJkxxtb"
        }

        # 如果今天填过健康卡，附带一个实体ID，更新实体
        today_submit_id = self._get_today_submit_id()

        if today_submit_id:
            post_dict['id'] = today_submit_id

        print("---- POST CARD DICT ----")
        print(post_dict)

        self._SESSION.post(self._HEALTHY_CARD_POST_PATH, json={'entity': post_dict})

    def get_user_info(self):
        r = self._SESSION.get(
            'https://work.zcst.edu.cn/default/base/workflow/com.sudytech.work.jluzh_LoginUser.jluzhLogin.LoginUser.jluzhUtil.biz.ext')
        resp_dict = json.loads(r.content.decode(encoding='utf-8'))
        print(resp_dict)

        self._USER_ID = str(resp_dict['result']['EMPID'])  # 用户ID
        self._ORG_ID = str(resp_dict['result']['ORGID'])  # 应该是学院ID
        self._ORG_NAME = resp_dict['result']['ORGNAME']  # 学院名称
        self._USER_REAL_NAME = resp_dict['result']['EMPNAME']  # 用户真实姓名
        self._USER_STUDENT_ID = resp_dict['result']['EMPCODE']  # 用户学号

    def _get_today_submit_id(self):
        try:
            return self._get_today_submit()['TODAY_SUBMIT_ID']
        except:
            return None

    def get_today_submit_time(self):
        try:
            return self._get_today_submit()['TODAY_SUBMIT_TIME']
        except:
            return None

    def _get_today_submit(self):
        r = self._SESSION.post(self._HEALTHY_CARD_QUERY_TODAY_PATH)
        resp_dict = json.loads(r.content.decode(encoding='utf-8'))
        print('TODAY SUBMIT')
        print(resp_dict)
        return {
            'TODAY_SUBMIT_ID': resp_dict['result'].get('ID', None),
            'TODAY_SUBMIT_TIME': resp_dict['result'].get('TJSJ', 'UNKNOWN')
        }

    @staticmethod
    def _get_fmt_date():
        now = datetime.now()
        return now.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")

    @staticmethod
    def _get_fmt_date_time():
        now = datetime.now()
        return now.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
