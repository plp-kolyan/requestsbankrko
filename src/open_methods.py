import os
from random import choice
from jsoncustom import JsonCustom
from zip_functions import create_path_is_not_exists


def return_listdir_open_json(JSON_TEST_OPEN_BASE_DIR):
    return os.listdir(path=f'{JSON_TEST_OPEN_BASE_DIR}')


def check_is_exists(response_id, JSON_TEST_OPEN_BASE_DIR):
    create_path_is_not_exists(JSON_TEST_OPEN_BASE_DIR)
    return f'{response_id}.json' not in return_listdir_open_json(JSON_TEST_OPEN_BASE_DIR)


def create_json(response_id: str, inns: list, JSON_TEST_OPEN_BASE_DIR):
    if check_is_exists(response_id, JSON_TEST_OPEN_BASE_DIR) is True:
        try:
            open(f'{JSON_TEST_OPEN_BASE_DIR}{response_id}.json', 'a').close()
            JC = JsonCustom(f'{JSON_TEST_OPEN_BASE_DIR}{response_id}.json')
            JC.data = {'id': response_id,
                       'status': 'done',
                       'result':
                           {'inns': [
                               {'inn': inn, 'inn_status': choice(('success', 'fail'))} for inn in inns]}}
            JC.write()
        except OSError:
            print('Failed creating the file')
        else:
            pass

    return response_id
