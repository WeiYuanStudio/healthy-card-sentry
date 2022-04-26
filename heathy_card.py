import json
import logging
from datetime import datetime, timezone, timedelta
from requests import get

_HEALTHY_CARD_QUERY_LOCATION_PATH = 'https://xmt.zcst.edu.cn/cms/items/区划信息'


def get_code_from_name(name: str, level: int):
    r = get(_HEALTHY_CARD_QUERY_LOCATION_PATH, params={
        'fields': ['id', 'code'],
        'filter': json.dumps({
            'level': {'_eq': level},
            'name': {'_eq': name}
        })
    })
    if r.status_code != 200:
        return None
    if len(r.json()['data']) > 0:
        return (r.json()['data'][0]['id'], r.json()['data'][0]['code'])
    else:
        return None


def get_code_by_name_and_parent_id(parent_id: int, name: str, level: int):
    r = get(_HEALTHY_CARD_QUERY_LOCATION_PATH, params={
        'fields': ['id', 'code'],
        'filter': json.dumps({
            'level': {'_eq': level},
            'name': {'_eq': name},
            'parent_id': {'_eq': parent_id}
        })
    })
    if r.status_code != 200:
        return None
    if len(r.json()['data']) > 0:
        return (r.json()['data'][0]['id'], r.json()['data'][0]['code'])
    else:
        return None


class Card:
    _HEALTHY_CARD_PRESET_DICT_PATH = 'https://work.zcst.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.work.jlzh.jkxxtb.jkxxcj.queryEmp.biz.ext'
    _HEALTHY_CARD_POST_PATH = 'https://work.zcst.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.portalone.base.db.saveOrUpdate.biz.ext'
    _HEALTHY_CARD_QUERY_TODAY_PATH = 'https://work.zcst.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.work.jlzh.jkxxtb.jkxxcj.queryToday.biz.ext'

    def __init__(self, session):
        self._SESSION = session

        user_info_dict = self._get_user_info()  # 获取用户个人信息
        preset_dict = self._load_preset()  # 加载表单预设

        logging.info('merge 2 dict')
        dict_merge = {**user_info_dict, **preset_dict}  # user info merge form preset
        logging.info(dict_merge)

        post_dict_need_csv = self._create_post_dict(dict_merge)

        logging.info('create post dict with merge dict')
        logging.info(post_dict_need_csv)

        self.form_dict = post_dict_need_csv  # form dict need csv data

    def _load_preset(self):
        logging.info('load user data from last commit')

        r = self._SESSION.post(self._HEALTHY_CARD_PRESET_DICT_PATH)

        resp_dict = json.loads(r.content.decode(encoding='utf-8'))

        result = resp_dict.get('result', None)
        logging.info(result)

        return result

    def _create_post_dict(self, user_data):
        data = {
            'sqrid': user_data['empid'],
            'sqbmid': user_data['orgid'],
            'fdygh': None,
            'rysf': user_data['qq'],  # 学生
            'bt': f'{self._get_fmt_date()} {user_data["empname"]} 健康卡填报',  # 标题
            'sqrmc': user_data['empname'],
            "gh": user_data['empcode'],
            "xb": None,
            "sqbmmc": user_data['orgname'],
            "nj": None,
            "zymc": None,
            "bjmc": None,
            "fdymc": None,
            "ssh": None,
            "lxdh": None,  # self._STUDENT_PHONE,
            "tbrq": self._get_fmt_date(),
            "tjsj": self._get_fmt_date_time(),
            "xjzdz": None,
            "jqqx": None,  # 假期期间去向 Todo: 上移到init
            "sfqwhb": "否",  # 去往湖北
            "sfjwhy": "否",
            "sfjwhygjdq": "",
            "xrywz": None,  # self._LOCATION_TYPE,
            "pcode": None,  # self._PROVINCE_CODE,
            "ccode": None,  # self._CITY_CODE,
            "dcode": None,  # self._COUNTY_CODE,
            "jtdz": None,  # self._LOCATION_DETAILED,
            "grjkzk": "1",  # 健康码
            "jrtw": "36",  # 体温
            "hsjcsj": None,  # self.VACCINATION_DATE,  # 最后接种日期 "2022-03-30"
            "ymjzqk": "已完成三针接种",
            "ymjzqkyy": "",
            "qsjkzk": "1",  # 亲属状况
            "jkqk": "1",  # 其他症状
            "cn": [
                "本人承诺登记后、到校前不再前往其他地区"
            ],  # 承诺
            "bz": "无",  # 备注
            "_ext": "{}",
            "sfgx": "1",
            "pname": None,  # self._PROVINCE,  # 省
            "cname": None,  # self._CITY,  # 市
            "dname": None,  # self._COUNTY,  # 区
            "__type": "sdo:com.sudytech.work.jlzh.jkxxtb.jkxxcj.TJlzhJkxxtb"
        }

        for k, v in data.items():
            if v is None:
                data[k] = user_data.get(k, None)
        return data

    def submit(self, csv_data: dict):
        # load data from csv, if did not exist in preset post dict

        for k, v in self.form_dict.items():
            if v is None:
                self.form_dict[k] = csv_data.get(k, None)

        # 如果今天填过健康卡，附带一个实体ID，更新实体
        today_submit_id = self._get_today_submit_id()

        if today_submit_id:
            self.form_dict['id'] = today_submit_id

        logging.info("posting card")
        logging.info(self.form_dict)
        self._SESSION.post(self._HEALTHY_CARD_POST_PATH, json={'entity': self.form_dict})
        logging.info("posted card success")

    def _get_user_info(self):
        logging.info('get user info')

        r = self._SESSION.get(
            'https://work.zcst.edu.cn/default/base/workflow/com.sudytech.work.jluzh_LoginUser.jluzhLogin.LoginUser.jluzhUtil.biz.ext')
        resp_dict = json.loads(r.content.decode(encoding='utf-8'))
        logging.info(resp_dict)

        # WARN: this dict key need to lower case
        user_dict_upper = resp_dict.get('result', None)

        logging.info(user_dict_upper)

        user_dict_lower = {}

        if user_dict_upper:
            for k, v in user_dict_upper.items():
                user_dict_lower[k.lower()] = v

        logging.info('trans user info to lower case')
        logging.info(user_dict_lower)

        return user_dict_lower

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
        logging.info('TODAY SUBMIT')
        logging.info(resp_dict)
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
