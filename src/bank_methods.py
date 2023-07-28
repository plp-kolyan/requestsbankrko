import os
import time
from datetime import timezone
from jsoncustom import JsonCustom
from dotenv import load_dotenv, dotenv_values
from requestsgarant import (
    RequestsGarant, RequestsGarantTestBaseUrl, RequestsGarantTestEndpoint, RequestsGarantTestHeaders
)

main_env = load_dotenv()

if 'PATH_TO_ENV' in dotenv_values(".env"):
    load_dotenv(dotenv_path=os.environ.get('PATH_TO_ENV'))
else:
    load_dotenv(dotenv_path='C:\\config_bank_rko\\.env')

inn_freedom = "Свободен"
inn_busy = "Занят"
test = True


def get_rand_str(total: int):
    import string
    import random
    rand_str = ''
    while len(rand_str) < total:
        rand_str += random.choice(string.ascii_letters + string.hexdigits)
    return rand_str


class Alfa(RequestsGarantTestHeaders):
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    dict_key = {'API-key': os.environ.get('alfabank_dict_key')}
    dict_key_test = {'API-key': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'}

    def __init__(self, test=test):
        super().__init__()
        self.test = test
        self.url = 'https://partner.alfabank.ru/public-api/v2/'


class CityBankes:

    cities_path_project = 'tests\cityesjson'


    def __init__(self):
        self.cities_path = f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\{self.cities_path_project}'
        self.JC = JsonCustom(f'{self.cities_path}\{self.__class__.__name__}.json')


    def do_json(self):
        if self.define_valid_json() == True:
            self.JC.data = self.response_json
            self.JC.write()
            return self.JC.data

    def define_valid_json(self):
        return True



class AlfaCity(CityBankes, Alfa):
    def __init__(self):
        Alfa.__init__(self)
        CityBankes.__init__(self)
        self.test = False

    def get_response(self):
        import requests
        return requests.get('https://partner.alfabank.ru/public-api/v2/dictionaries?code=cities', headers=self.headers)

    def define_valid_json(self):
        if 'values' in self.response_json:
            return True


class AlfaStatusLead(Alfa):
    def __init__(self, json, test=test):
        super().__init__(test)
        self.params = json
        self.url += 'leads'
        self.method = 'get'


class AlfaScoring(Alfa):
    def __init__(self, json, test=test):
        super().__init__(test)
        self.json = json
        self.url += 'checks'
        self.method = 'post'

    def get_status_inn(self, status_cod, status_inn):
        if self.response.status_code == status_cod:
            self.success = True
            return status_inn

    def do_json(self):
        if (self.test is True) and ('error' in self.response_json):
            if self.response_json['error'] == 'Internal Server Error':
                return self.get_status_inn(500, inn_busy)
        return self.get_status_inn(403, inn_busy)

    def do_status_code(self):
        return self.get_status_inn(200, inn_freedom)


class AlfaLead(Alfa):
    def __init__(self, json, test=test):
        super().__init__(test)
        self.limit_error = False
        self.method = 'post'
        self.json = json
        self.url += 'leads'

    def do_json(self):
        if 'id' in self.response_json:
            self.success = True
            return self.response_json['id']
        if 'errors' in self.response_json:
            if len(self.response_json['errors']) != []:
                if 'code' in self.response_json['errors'][0]:
                    code = self.response_json['errors'][0]['code']
                    if code == 'UNACCEPTABLE_COMPANY':
                        self.success = True
                        return 'Клиент занят другими'
                    if code == 'LEADS_LIMIT_ERROR':
                        self.limit_error = True
                        self.success = True
                        return 'Превышен лимит'
                    if code == 'validationError':
                        self.success = True
                        if 'detail' in self.response_json['errors'][0]:
                            return self.response_json['errors'][0]['detail']


class VTBBigFather(RequestsGarant):
    path_vtb_token = f'{os.path.abspath(os.curdir)}/vtb_api_token.json'.replace('venv\Lib\site-packages/', '')
    credits = {
        'grant_type': os.environ.get('vtb_grant_type'),
        'client_id': os.environ.get('vtb_client_id'),
        'client_secret': os.environ.get('vtb_client_secret')
    }

    def __init__(self):
        import urllib3
        urllib3.disable_warnings()
        super().__init__()
        # self.cert = f'{os.path.abspath(os.curdir)}/src/certs.pem'
        self.verify = False
        self.url = 'https://gw.api.vtb.ru:443/openapi/smb/lecs/lead-impers/v1/'


class Aut:
    args_token_cls = ()
    def __init__(self, token_cls, ERROR_AUT_KEY_VAL_CHOICES):
        self.path_token = f'{os.path.abspath(os.curdir)}/{token_cls.__name__}.txt'.replace('venv\Lib\site-packages/', '')
        self.token_cls = token_cls
        self.ERROR_AUT_KEY_VAL_CHOICES = ERROR_AUT_KEY_VAL_CHOICES

    def exist_error_authorization(self):
        for key, values in self.ERROR_AUT_KEY_VAL_CHOICES:
            if key in self.response_json:
                if self.response_json[key] == values:
                    return True

    def write_token(self):
        token_obj = self.token_cls(*self.args_token_cls)
        rezult = token_obj.get_rezult()
        if token_obj.success is True:
            with open(self.path_token, 'w') as file:
                file.write(rezult)
            return rezult

    def get_token(self):
        while True:
            try:
                with open(self.path_token, 'r') as file:
                    return file.read()
            except:
                time.sleep(3)
                self.write_token()

    def do_json(self):
        if self.exist_error_authorization():

            if self.write_token() is not None:
                self.get_rezult()
                if self.success is True:
                    return self.rezult

        return self.do_json_success_authorization()






class VTBToken(VTBBigFather):
    def __init__(self):
        super().__init__()
        self.data = self.credits

        self.url = 'https://open.api.vtb.ru:443/passport/oauth2/token'
        self.method = 'post'

    def do_json(self):
        if 'access_token' in self.response_json:
            self.success = True
            return self.response_json['access_token']





class VTBFather(Aut, VTBBigFather):
    def __init__(self, json):
        VTBBigFather.__init__(self)
        ERROR_AUT_KEY_VAL_CHOICES = (

            ('reason', 'Unauthorized'),
            ('errorMessage', 'the header <Authorization> was not received in the request'),
            ('error', 'key not authorized: no matching policy found')
        )
        Aut.__init__(self, VTBToken, ERROR_AUT_KEY_VAL_CHOICES)
        self.method = 'post'
        self.json = json

    # def exist_error_authorization(self):
    #     for key, values in (
    #     ('reason', 'Unauthorized'), ('errorMessage', 'the header <Authorization> was not received in the request')):
    #         if key in self.response_json:
    #             if self.response_json[key] == values:
    #                 return True

    # def write_vtb_header(self):
    #     vtbtoken = VTBToken()
    #     rezult = vtbtoken.get_rezult()
    #     if vtbtoken.success is True:
    #         headers = {
    #             'X-IBM-Client-Id': self.credits['client_id'].replace('@ext.vtb.ru', ''),
    #             'Authorization': f'Bearer {rezult}'
    #         }
    #         JS = JsonCustom(self.path_vtb_token)
    #         JS.data = headers
    #         JS.write()
    #         return headers
    def do_status_code(self):
        if self.response_status_code == 404:
            self.resend_send = True
        return self.response_status_code

    def do_json_success_authorization(self):
        if ('leads' in self.response_json) and ((self.response.status_code == 200)
                or "Некорректный ИНН." in str(self.response_json)):
            self.success = True
            return self.response_json['leads']



    def get_response_production(self):
        self.args_request.update({'headers': {
                'X-IBM-Client-Id': self.credits['client_id'].replace('@ext.vtb.ru', ''),
                'Authorization': f'Bearer {self.get_token()}'
            }})
        return super().get_response_production()


class VTBStatusLead(VTBFather):
    def __init__(self, json):
        super().__init__(json)
        self.params = json
        self.url += 'leads'
        self.method = 'get'


class VTBScoring(VTBFather):
    def __init__(self, json):
        super().__init__(json)
        self.url += 'check_leads'

    def do_json_success_authorization(self):
        do_json_father = super().do_json_success_authorization()
        if do_json_father is None:
            if 'moreInformation' in self.response_json:
                if self.response_json['moreInformation'] == 'URL Open error: Could not connect to endpoint' or \
                        self.response_json['moreInformation'] == 'Internal Server Error: ' \
                                                                 'Assembly reference is required.' or \
                        self.response_json['moreInformation'].find('<BackErr>') != -1:
                    self.resend_send = True
        return do_json_father


class VTBLead(VTBFather):
    def __init__(self, json, test=test):
        super().__init__(json)
        self.test = test
        self.custom_test = True
        self.url += 'leads_impersonal'

    def define_json_response_test(self):
        data = [{'leadId': lead['sourceLeadId'], 'status': 'NEW',
                 'sourceLeadId': lead['sourceLeadId'], 'responseCode': 'SUCCESS',
                 'responseCodeDescription': 'Операция выполнена успешно'} for lead in self.json['leads']]

        self.json_response_test = {"leads": data}


class Open(RequestsGarantTestEndpoint):
    base_url = 'https://openpartners.ru/api/v2/request/'
    JSON_TEST_OPEN_BASE_DIR = f'{os.path.abspath(os.curdir)}/jsons/'
    token = os.environ.get('open_token')

    def __init__(self):
        super().__init__()
        self.test = test
        self.headers = {
            # 'Host': 'openpartners.ru',
            # 'Content-Type': 'multipart/form-data',
            'X-Auth-Token': self.token
        }


class OpenStatusLead(Open):
    endpoint = 'status'
    endpoint_test = 'status/test'

    def __init__(self, json, test=test):
        super().__init__()
        self.params = json
        self.method = 'get'
        self.test = test


class OpenLeadScoring(Open):
    def __init__(self, json, test=test):
        super().__init__()
        self.json = json
        self.custom_test = True
        self.test = test


class OpenCity(CityBankes, RequestsGarant):
    def __init__(self):
        RequestsGarant.__init__(self)
        CityBankes.__init__(self)
        self.url = Open.base_url.strip('request/') + '/dictionaries/city'
        self.headers = Open().headers
        self.method = 'get'

class OpenScoring:
    def __init__(self, json, test=test):
        self.json = json
        self.test = test
        self.success = False
        self.rezult = None

    def get_rezult(self):
        osid = OpenScoringID(self.json, self.test)
        osid.get_rezult()
        self.rezult = osid.rezult
        self.resend_send = osid.resend_send
        self.args_request = osid.args_request
        if osid.success:
            for i in range(10):
                osstatus = OpenScoringStatus({'id': f'{osid.rezult}'}, self.test)
                osstatus.get_rezult()
                self.resend_send = osstatus.resend_send
                self.args_request = osstatus.args_request
                self.rezult = osstatus.rezult
                if osstatus.success:
                    self.success = True
                    return self.rezult
                time.sleep(10)
            self.resend_send = True
            return self.rezult
        else:
            self.rezult = osid.rezult
            return self.rezult


class OpenScoringID(OpenLeadScoring):
    endpoint = 'getduplicates'
    endpoint_test = 'getduplicates/test'

    def __init__(self, json, test=test):
        super().__init__(json, test)
        self.method = 'post'

    def define_json_response_test(self):
        from open_methods import create_json

        self.json_response_test = {
            'id': f'{get_rand_str(8)}-{get_rand_str(4)}-{get_rand_str(4)}-{get_rand_str(4)}-{get_rand_str(12)}'
        }
        create_json(self.json_response_test['id'], self.json['inns'], self.JSON_TEST_OPEN_BASE_DIR)

    def do_json(self):
        if 'id' in self.response_json:
            self.success = True
            return self.response_json['id']


class OpenScoringStatus(OpenLeadScoring):
    endpoint = OpenScoringID.endpoint
    endpoint_test = OpenScoringID.endpoint_test

    def __init__(self, json, test=test):
        super().__init__(json, test)
        self.method = 'get'
        self.params = self.json

    def define_json_response_test(self):
        self.json_response_test = JsonCustom(
            f'{self.JSON_TEST_OPEN_BASE_DIR}{self.json["id"]}.json').reed()

    def do_json(self):
        if 'result' in self.response_json:
            self.success = True
            return self.response_json['result']['inns']


class OpenLead(OpenLeadScoring):
    endpoint = 'add'
    endpoint_test = 'add/test'

    def __init__(self, json, test=test):
        super().__init__(None, test)
        self.method = 'post'
        self.data = json

    def define_json_response_test(self):
        self.json_response_test = {
            'id': f'{get_rand_str(8)}-{get_rand_str(4)}-{get_rand_str(4)}-{get_rand_str(4)}-{get_rand_str(12)}',
            'status': 'inqueue'
        }

    def do_json(self):
        if 'id' in self.response_json:
            self.success = True
            return self.response_json['id']


class Module(RequestsGarantTestBaseUrl):
    base_url = 'https://partner.modulbank.ru/public/'
    base_url_test = 'https://partnertest.modulbank.ru/public/'
    tnx = os.environ.get('module_tnx')

    def __init__(self):
        super().__init__()


class ModuleLead(Module):
    endpoint = f'agent/app/add?tnx={Module.tnx}'

    def __init__(self, json, test=test):
        super().__init__()
        self.method = 'post'
        self.json = json
        self.test = test
        self.custom_test = True
        self.headers = {
            'Method': 'POST',
            'Content-Type': 'application/json'
        }

    def define_json_response_test(self):
        self.json_response_test = {
            "status": "ok",
            "response": {
                "list": [
                    {
                        "id": f'{get_rand_str(8)}-{get_rand_str(4)}-{get_rand_str(4)}-{get_rand_str(4)}-{get_rand_str(12)}',
                        'inn': self.json['inn']
                    }
                ]
            },
            "_requestid": "4A40616B-3B75-46E4-9318-17DEFB38555F",
            "access": []
        }

    def do_json(self):
        if 'response' in self.response_json:
            if 'list' in self.response_json['response']:
                if self.response_json['response']['list']:
                    for dict_response in self.response_json['response']['list']:
                        if dict_response['inn'] == self.json['inn']:
                            self.success = True
                            return dict_response['id']


class Tochka(RequestsGarant):
    token = os.environ.get('tochka_token')

    def __init__(self, json):
        super().__init__()
        self.url = 'https://open.tochka.com:3000/rest/v1/'
        self.json = json
        self.json['token'] = self.token


class TochkaStatusLead(Tochka):
    def __init__(self, json):
        super().__init__(json)
        self.method = 'post'
        self.url += 'request/statuses'


class TochkaLead(Tochka):
    def __init__(self, json):
        super().__init__(json)
        self.method = 'post'
        self.url += 'request/new'
        self.double = False

    def do_json(self):
        if isinstance(self.response_json, list):
            if self.response_json:
                if 'Не удалось определить пол' in self.response_json[0]:
                    self.json['request'].update({'sex': 'M'})
                    return self.get_rezult()
                elif 'Заполненная заявка является дублем' in self.response_json[0]:
                    self.double = True

                self.success = True
                return self.response_json[0]

        if 'data' in self.response_json:
            self.success = True
            return self.response_json['data']


class TochkaRegistryUr(Tochka):
    def __init__(self, json):
        super().__init__(json)
        self.method = 'post'
        self.url += 'request/registration'

    def do_json(self):
        if isinstance(self.response_json, dict):
            if self.response_json:
                self.success = True
                return self.response_json


class TochkaAddDocs(Tochka):
    def __init__(self, json):
        super().__init__(json)
        self.json['request']['zip'] = self.make_zip()
        self.method = 'post'
        self.url += 'request/add_files'

    def make_zip(self):
        from zip_functions import make_zip
        return make_zip(self.json['request']['zip'])

    def do_json(self):
        if isinstance(self.response_json, dict):
            if self.response_json:
                self.success = True
                return self.response_json

def get_recaptcha_v2(proxy):
    from twocaptcha import TwoCaptcha

    solver = TwoCaptcha(os.environ.get('rucaptcha_key'))
    result = solver.recaptcha(sitekey='6LcZ1zIUAAAAAIdX_hL_-LgO6OXS1nMEM8-E-E8m',
                              url='https://www.google.com/recaptcha/api2/bframe?hl=en&v=Km9gKuG06He-isPsP6saG8cn&k=6LcZ1zIUAAAAAIdX_hL_-LgO6OXS1nMEM8-E-E8m',
                              proxy={'type': 'HTTPS', 'uri': proxy}
                              )

    return result

class TochkaLeedRef(RequestsGarant):
    def __init__(self, json):
        super().__init__()
        self.data = json

        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '2553',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'forms.tildacdn.com',
            'Origin': 'https://partner.tochka.com',
            'Pragma': 'no-cache',
            'Referer': 'https://partner.tochka.com/',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

        }
        self.method = 'post'
        self.url = 'https://forms.tildacdn.com/procces/'
        # self.proxy = proxy
        # self.proxies = {'https': f'http://{self.proxy}/'}
        self.needcaptcha = False

    def do_json(self):
        if 'needcaptcha' in self.response_json:
            self.needcaptcha = True
        elif 'results' in self.response_json:
            self.success = True
            return str(self.response_json['results'])


    # def get_rezult(self):
    #     s = super(TochkaLeedRef, self).get_rezult()
    #     print(s)
    #     return s

#         {"needcaptcha":1}
# 'sitekey' : '6LcZ1zIUAAAAAIdX_hL_-LgO6OXS1nMEM8-E-E8m',




class MoeDelo(RequestsGarantTestHeaders):
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    username = os.environ.get('moedelo_username')
    user_key = os.environ.get('moedelo_user_key')

    def __init__(self, test=test):
        super().__init__()
        self.custom_test = False
        self.test = test
        self.url = 'https://public.moedelo.org/Home/api/Registration/ExternalRegistration/V2'
        self.dict_key = self.genheaders(self.username, self.user_key)
        self.dict_key_test = self.dict_key

    @staticmethod
    def genheaders(user_name, user_key):
        import uuid
        import hashlib
        import datetime
        import base64
        random = str(uuid.uuid4()).encode('ASCII')
        nonce = random
        curdate = datetime.datetime.now(tz=timezone.utc).replace(microsecond=0)

        hash_digest = hashlib.sha1()
        hash_digest.update(nonce)
        hash_digest.update(curdate.isoformat().encode())
        hash_digest.update(user_key.encode())

        x_wsse = ', '.join(['UsernameToken Username="{user}"',
                            'PasswordDigest="{digest}"',
                            'Nonce="{nonce}"',
                            'Created="{created}"'])
        x_wsse = x_wsse.format(
            user=user_name,
            digest=base64.b64encode(hash_digest.digest()).decode('utf-8'),
            nonce=base64.b64encode(nonce).decode('utf-8'),
            created=curdate.isoformat(),
        )
        return {
            'X-WSSE': x_wsse,
        }


class MoeDeloLead(MoeDelo):
    def __init__(self, json, test=test):
        super().__init__(test)
        self.method = 'post'
        self.json = json

    def define_json_response_test(self):
        self.json_response_test = {"RequestId": "588-008-189"}

    def do_json(self):
        if 'RequestId' in self.response_json:
            self.success = True
            return self.response_json['RequestId']
        elif 'К сожалению, такой лид уже зарегистрирован' in self.response_json:
            self.success = True
            return self.response_json
        elif 'ValidationErrors' in self.response_json:
            self.success = True
            return self.response_json['ValidationErrors']


def get_url(mod):
    return f"https://api.raiffeisen.ru/openapi-013-{mod}/corporate-leads-xs/app"


class Raifazen(RequestsGarantTestBaseUrl):
    endpoint = ''
    base_url = get_url('opn')
    base_url_test = get_url('snd')
    token = os.environ.get('raifazen_token')
    partner_id = os.environ.get('raifazen_partner_id')

    def __init__(self, json, test=test):
        super().__init__()
        self.headers = {
            'key': self.token,
            'partnerID': self.partner_id
        }

        self.method = 'post'
        self.test = test
        self.json = json


class PSBall(RequestsGarantTestBaseUrl):
    # base_url = 'https://api.lk.psbank.ru/fo/v1.0.0'
    base_url = 'https://api.lk.psb.services/fo/v1.0.0'
    # base_url = 'https://api.lk.psb.services/fo/v1.0.0'
    base_url_test = 'https://api.lk.finstar.online/fo/v1.0.0'

    def __init__(self, test):

        super().__init__()
        # self.session = session
        self.test = test




# class PSBall:
#     def __init__(self):
#         self.test = test
#         if test is True:
#             self.url = 'https://api.lk.finstar.online/fo/v1.0.0'
#         else:
#             self.url = 'https://api.lk.psbank.ru/fo/v1.0.0'


class PSBToken(PSBall):
    def __init__(self, test):
        super().__init__(test)
        self.method = 'post'
        # self.data = {"email": "andrevo@bk.ru", "password": "0831254Aa."}
        self.data = {"email": os.environ.get('psb_email'), "password": os.environ.get('psb_password')}
        self.endpoint = '/user/login'

    def do_json(self):
        if 'data' in self.response_json:
            data = self.response_json['data']
            if 'access_token' in data:
                self.success = True
                return data['access_token']



    # def get_response(self):
    #     return self.session.post(f'{self.url}/user/login', data={"email": "andrevo@bk.ru", "password": "0831254Aa."})


class PSBParent(Aut, PSBall):

    def __init__(self, test=test):
        PSBall.__init__(self, test)
        ERROR_AUT_KEY_VAL_CHOICES = (('name', 'Unauthorized'),)
        Aut.__init__(self, PSBToken, ERROR_AUT_KEY_VAL_CHOICES)
        self.args_token_cls = (test,)



    def do_json_success_authorization(self):
        if 'status' in self.response_json:
            if self.response_json['status'] == 429:
                time.sleep(3)
                return self.get_rezult()
        return self.do_json_wrapper()

    def get_response_production(self):
        self.args_request.update({'url': f'{self.url}?access-token={self.get_token()}'})
        r = super().get_response_production()
        return r

    def do_json_wrapper(self):
        return self.response_json


class PSBScoring(PSBParent):


    def __init__(self, json_dict, test=test):
        super().__init__(test)
        self.json = json_dict
        self.endpoint = f'/orders/check-inn'
        self.method = 'post'


    def do_json_wrapper(self):
        if 'status' in self.response_json:
            if self.response_json['status'] == 'NOT_EXISTS':
                self.success = True
                return inn_freedom
            elif self.response_json['status'] == 'ALREADY_EXISTS':
                self.success = True
                return inn_busy


class PSBdfmqueue(PSBParent):
    def __init__(self, json_dict, test):
        super().__init__(test)
        self.json = json_dict
        self.endpoint = f'/dfm/queue'
        self.method = 'post'

    def do_json_wrapper(self):
        queue_id = self.response_json.get('queue_id')
        if queue_id is not None:
            self.success = True
            return queue_id



class PSBdfmqueueid(PSBParent):
    def __init__(self, id, test):
        super().__init__(test)
        self.method = 'get'
        self.endpoint = f'/dfm/queue/{id}'
        self.in_que = False

    def do_json_wrapper(self):
        status, data = (self.response_json.get(key) for key in ['status', 'data'])

        if status == 'завершено' and isinstance(data, list):
            self.success = True
            return data

        elif status == 'в обработке':
            self.in_que = True



class PSBLead(PSBParent):


    def __init__(self, json_dict, test=test):
        super().__init__(test)
        self.json = json_dict
        self.endpoint = f'/orders'
        self.method = 'post'

    def do_json_wrapper(self):
        if 'data' in self.response_json:
            if 'id' in self.response_json['data']:
                self.success = True
                return self.response_json['data']['id']

        elif 'errors' in self.response_json:
            if 'message' in self.response_json['errors']:
                if self.response_json['errors']['message'] == 'inn: В системе найден дубликат.':
                    self.success = True
                    return inn_busy

class RosBankLead(RequestsGarant):
    def __init__(self, json):
        super().__init__()
        self.url = 'https://api.rosbank.ru/private-person/agent-pro-request/request/index'
        self.method = 'post'
        self.json = json
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Referer': "https://www.rosbank.ru/",
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,ja;q=0.5',
            'Content-Type': "application/json;",
            'Origin': "https://www.rosbank.ru",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-site",

        }

    def do_json(self):
        if 'success' in self.response_json:
            if 'id' in self.response_json:
                self.success = True
                return self.response_json['id']


class Kontur(RequestsGarantTestBaseUrl):
    base_url = 'https://api-crm-billing.kontur.ru'
    base_url_test = 'https://api-billy-crm.testkontur.ru/'


    def __init__(self, json, test):
        super().__init__()
        self.test = test
        self.json = json
        self.headers = {'x-Auth-CustomToken': os.environ.get('kontur_token_test') if test else os.environ.get('kontur_token_prod')}

    def do_json(self):
        self.prospective_sale_id = self.response_json.get('ProspectiveSaleId')
        if self.prospective_sale_id is not None:
            self.success = True
            return self.suc_resp()
        results = self.response_json.get('Results')
        if results is not None:
            if results:
                message = results[0].get('Message')
                if message is not None:
                    if message in self.invalids:
                        self.success = True
                        return inn_busy


class KonturCanCreate(Kontur):
    invalids = [
        'Есть такая же потенциальная продажа в запрашиваемом PartnerCode',
        'Есть такая же потенциальная продажа в другом PartnerCode'
    ]
    def __init__(self, json, test):
        super().__init__(json, test)
        self.endpoint = '/prospectivesales/cancreate/v2'
        self.method = 'post'


    def suc_resp(self):
        return inn_freedom







class KonturProspectiveSales(Kontur):
    invalids = ['Потенциальная продажа с таким Id уже существует']
    def __init__(self, json, test):
        super().__init__(json, test)
        self.endpoint = '/prospectivesales/create/v4'
        self.method = 'post'


    def suc_resp(self):
        return self.prospective_sale_id


def mutation_inn(inn: str):
    inn = str(inn)
    if len(inn) in [9, 11]:
        inn = '0' + inn
    return inn

