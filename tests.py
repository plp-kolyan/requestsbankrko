from unittest import TestCase
import json
from requestsgarant import return_test_response

from src.bank_methods import *

class TestTestCase(TestCase):
    def test_0(self):
        with open('requestsbankrko.log', 'r') as file:

            for json_str in file.read().splitlines():
                # print(json.loads(json_str)['message'])
                obj = VTBScoring({})
                obj.response_json = json.loads(json_str)['message']
                obj.do_json()
                if not obj.resend_send:
                    print(obj.response_json)
                    return

            print('Нет не отработанных ошибок')

                # print(json.loads(json.loads(json_str)['message']))


