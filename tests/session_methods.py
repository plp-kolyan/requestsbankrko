import datetime
import os
import pickle
import requests


SESSION_BASE_DIR = os.environ.get('SESSION_BASE_DIR')


def return_current_date():
    return str(datetime.datetime.now().date())


def return_listdir_requests_session():
    return os.listdir(path=f'{SESSION_BASE_DIR}requests_session\\')


def check_is_exists():
    return f'session_{return_current_date()}.txt' not in return_listdir_requests_session()


class DefineTodaySession:
    def __init__(self):
        self.path = f'{SESSION_BASE_DIR}requests_session\\'

    @staticmethod
    def create():
        return requests.session()

    def open_to_write(self, function_obj):
        test_pickle_dump = open(
            rf'{self.path}session_{return_current_date()}.txt', 'wb')
        function_obj(self.create(), test_pickle_dump)
        test_pickle_dump.close()
        print('Session successfully create!')

    def write(self):
        if check_is_exists() is True:
            self.open_to_write(pickle.dump)
        else:
            print('Session already exists!')


class LoadSession:
    def __init__(self):
        self.current_session = ''
        self.path = f'{SESSION_BASE_DIR}requests_session\\'

    @property
    def return_token(self):
        with open(f'{self.path}token.txt', 'r') as filetoken:
            return filetoken.read()

    def loading(self):
        test_pickle_dump = open(rf'{self.path}session_{return_current_date()}.txt', 'rb')
        self.current_session = pickle.load(test_pickle_dump)
        test_pickle_dump.close()

    def get(self):
        self.loading()
        return self.current_session
