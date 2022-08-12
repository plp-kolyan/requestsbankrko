import os
import time
from datetime import timezone
from jsoncustom import JsonCustom
from dotenv import load_dotenv
from requestsgarant import (
    RequestsGarant, RequestsGarantTestBaseUrl, RequestsGarantTestEndpoint, RequestsGarantTestHeaders
)


load_dotenv()
path_to_env = os.environ.get('path_to_env')
if path_to_env:
    load_dotenv(dotenv_path=path_to_env)


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
    cities_path = os.environ.get('cities_path')

    def __init__(self):
        self.JC = JsonCustom(f'{self.cities_path}{self.__class__.__name__}.json')

    def do_json(self):
        if self.define_valid_json() == True:
            self.JC.data = self.response_json
            self.JC.write()
            return self.JC.data


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
    path_vtb_token = f'{os.path.abspath(os.curdir)}/vtb_api_token.json'
    credits = {
        'grant_type': os.environ.get('vtb_grant_type'),
        'client_id': os.environ.get('vtb_client_id'),
        'client_secret': os.environ.get('vtb_client_secret')
    }

    def __init__(self):
        super().__init__()
        self.url = 'https://epa.api.vtb.ru/openapi/smb/lecs/lead-impers/v1/'


class VTBToken(VTBBigFather):
    def __init__(self):
        super().__init__()
        self.data = self.credits
        self.url = 'https://passport.api.vtb.ru/passport/oauth2/token'
        self.method = 'post'

    def do_json(self):
        if 'access_token' in self.response_json:
            self.success = True
            return self.response_json['access_token']


class VTBFather(VTBBigFather):
    def __init__(self, json):
        super().__init__()
        self.method = 'post'
        self.json = json

    def exist_error_authorization(self):
        for key, values in (('status', 'needConfirm'), ('httpMessage', 'Unauthorized')):
            if key in self.response_json:
                if self.response_json[key] == values:
                    return True

    def write_vtb_header(self):
        vtbtoken = VTBToken()
        rezult = vtbtoken.get_rezult()
        if vtbtoken.success is True:
            headers = {'Authorization': f'Bearer {rezult}'}
            JS = JsonCustom(self.path_vtb_token)
            JS.data = headers
            JS.write()
            return headers

    def do_json(self):
        if self.exist_error_authorization():
            response_vtb_token = self.write_vtb_header()
            if response_vtb_token is not None:
                self.get_rezult()
                if self.success is True:
                    return self.rezult

        if 'leads' in self.response_json:
            self.success = True
            return self.response_json['leads']

    def get_header(self):
        while True:
            try:
                return JsonCustom(self.path_vtb_token).reed()
            except:
                time.sleep(3)
                self.write_vtb_header()

    def get_response_production(self):
        self.args_request.update({'headers': self.get_header()})
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

    def do_json(self):
        do_json_father = super().do_json()
        if do_json_father is None:
            if 'moreInformation' in self.response_json:
                if self.response_json['moreInformation'] == 'URL Open error: Could not connect to endpoint' or \
                        self.response_json['moreInformation'] == 'Internal Server Error: ' \
                                                                 'Assembly reference is required.':
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


class OpenCity(CityBankes, Open):
    def __init__(self):
        Open.__init__(self)
        CityBankes.__init__(self)


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

    def do_json(self):
        if isinstance(self.response_json, list):
            if self.response_json:
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


class MoeDelo(RequestsGarantTestHeaders):
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    username = os.environ.get('moedelo_username')
    user_key = os.environ.get('moedelo_user_key')

    def __init__(self, test=test):
        super().__init__()
        self.custom_test = True
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


class PSBall:
    def __init__(self):
        self.test = test
        if test is True:
            self.url = 'https://api.lk.finstar.online/fo/v1.0.0'
        else:
            self.url = 'https://api.lk.psbank.ru/fo/v1.0.0'


class PSBToken(PSBall, RequestsGarant):
    def do_json(self):
        if 'data' in self.response_json:
            data = self.response_json['data']
            if 'access_token' in data:
                self.success = True
                return data['access_token']

    def get_response(self):
        return self.session.post(f'{self.url}/user/login', data={"email": "andrevo@bk.ru", "password": "0831254Aa."})


class PSBParent(RequestsGarantTestBaseUrl):
    base_url = 'https://api.lk.psbank.ru/fo/v1.0.0'
    base_url_test = 'https://api.lk.finstar.online/fo/v1.0.0'

    def __init__(self, test=test):
        super().__init__()
        self.test = test


class PSB(PSBParent):
    email = os.environ.get('psb_email')
    password = os.environ.get('psb_password')

    def __init__(self, session, test=test):
        super().__init__(test)
        self.session = session
        self.access_token = self.create_token()

    def create_token(self):
        for i in range(0, 3):
            self.access_token = self.get_rezult()
            if self.success is True:
                return self.access_token

    def get_response(self):
        return self.session.post(f'{self.url}/user/login', data={"email": self.email, "password": self.password})

    def receive_condition(self):
        if 'data' in self.response_json:
            data = self.response_json['data']
            if 'access_token' in data:
                self.success = True
                return data['access_token']
            else:
                return data


class PSBCity(PSB, CityBankes):
    def __init__(self, session):
        PSB.__init__(self, session)
        CityBankes.__init__(self)


class PSBScoring(PSB):
    endpoint = '/orders/check-inn?access-token='

    def __init__(self, json_dict, session, test=test):
        super().__init__(session, test)
        self.json = json_dict

    def get_response_production(self):
        return self.session.post(
            url=f'{self.url}{self.access_token}',
            json=self.json,
            timeout=5
        )

    def do_json(self):
        if 'data' in self.response_json:
            data = self.response_json['data']
            if 'access_token' in data:
                self.success = True
                return data['access_token']
            else:
                return data


class PSBLead(PSB):
    endpoint = '/orders?access-token='

    def __init__(self, json, session, test=test):
        super().__init__(session, test)
        self.json = json

    def get_response_production(self):
        return self.session.post(f"{self.url}{self.access_token}", json=self.json)

    def do_json(self):
        if 'data' in self.response_json:
            if 'id' in self.response_json['data']:
                self.success = True
                return self.response_json['data']['id']
            else:
                return self.response_json
