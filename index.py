import csv
import logging

from requests import Session

from secure import Secure
from heathy_card import Card
from notify import Notify


def main_handler(event, context):
    """云函数入口"""

    logging.getLogger().setLevel(logging.INFO)

    logging.info('script start up')
    logging.info('start read csv')

    with open('./user_data.csv') as f:
        logging.info('read csv finished')
        user_data_csv = csv.DictReader(f)
        logging.info('read csv finished, start execute all user')
        for csv_dict in user_data_csv:
            try:
                with Session() as session:
                    session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)'}  # 设置UA避免被防火墙拦截
                    logging.info(f'start trying login user:{csv_dict["login_id"]}')
                    login_state = Secure(csv_dict['login_id'], csv_dict['login_pwd'], session).login().test()
                    if login_state:
                        logging.info('login finished')
                    else:
                        logging.error(f'login user:{csv_dict["login_id"]} failed')
                        continue

                    card = Card(session)
                    logging.info('card init finished')

                    card.submit(csv_dict)
                    logging.info('card init finished')

                    today_submit_time = card.get_today_submit_time()

                    Notify().send('[OK]健康卡自动填报已执行', f'健康卡自动填报成功，从服务端查询到的最后填报时间为{today_submit_time}')
                    logging.info(f'[OK]健康卡:{csv_dict["login_id"]}自动填报成功，从服务端查询到的最后填报时间为{today_submit_time}')
            except Exception as e:
                print(e)
                Notify().send('[ERROR]健康卡自动填表发生错误', '健康卡自动填表发生错误，请到云函数平台检查执行日志，联系开发者并提供必要的错误日志')
                logging.error(f'[ERROR]健康卡:{csv_dict["login_id"]}自动填报失败')


if __name__ == '__main__':
    """本地调试"""
    main_handler(None, None)
