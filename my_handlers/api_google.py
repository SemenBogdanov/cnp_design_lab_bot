import sys

import gspread
import logging
from pprint import *
from fast_bitrix24 import *

# from create_bot import dp
from key import bitrix_key_rus


wh = f"https://pm.ac.gov.ru/rest/16/{bitrix_key_rus}/"
bx24 = Bitrix(wh)


def rec_to_sheets(data):
    fsa = "service_account.json"
    sa = gspread.service_account(fsa)
    sh = sa.open("Design_lab_orders")
    wsh = sh.worksheet('Data')
    id_val = wsh.acell('K2').value
    # logging.info(id_val)
    wsh.insert_row(list(data.values()), index=2)
    wsh.update('K2', int(id_val) + 1)
    # wsh.append_row(list(data.values()),table_range="A1")
    # wsh.append_row(list(data.values()))
    return True


def add_user_info(data):
    fsa = "service_account.json"
    sa = gspread.service_account(fsa)
    sh = sa.open("Design_lab_orders")

    wsh = sh.worksheet('Users')
    wsh.append_row(list(data.values()))
    return


def check_user(u_id: str):
    fsa = "service_account.json"
    sa = gspread.service_account(fsa)
    sh = sa.open("Design_lab_orders")
    wsh = sh.worksheet('Users')
    #     get A col values

    cnt_A = wsh.col_values(1)

    name_from_sheet = ""
    for i in cnt_A:
        # logging.info(i)
        if str(i) == str(u_id):
            name_from_sheet = wsh.row_values(cnt_A.index(i) + 1)[1]
    print(f'name_from_sheet is {name_from_sheet}')
    return name_from_sheet


async def create_new_bitrix_task(title: str, description: str, deadline, response_employer_id: int = 425, group_id: int = 377,
                           auditors='2300', creator: int = '16'):
        logging.disable(10)
        result_of_call = await bx24.call('tasks.task.add',
                      {'fields': {
                          'TITLE': title,
                          'DESCRIPTION': description,
                          'GROUP_ID': group_id,
                          'AUDITORS': auditors,
                          'DEADLINE': deadline,
                          'RESPONSIBLE_ID': response_employer_id,
                          'CREATED_BY': creator}
                      })
        # await bx24.call('task.stages.movetask',{'id':result_of_call['task']['id'],'stageId':'8750'})
        # print(f"Переменная res: {result_of_call['task']['id']}")
        return result_of_call


        # return result_of_call['task']['id']
        # logging.INFO(res['task']['id'])


