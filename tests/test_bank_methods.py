from src.bank_methods import *
import json
from pprint import pprint
from unittest import TestCase
import requests
from requests.models import Response
from requestsgarant import return_test_response


try:
    from session_methods import DefineTodaySession, LoadSession
except:
    from .session_methods import DefineTodaySession, LoadSession


PATH_TO_VTB_JSON = 'C:\\CustomMethods\\bankes\\VTBtoken_test.json'
PATH_TO_VTB_CITY_JSON = 'C:\\CustomMethods\\bankes\\cityes\\VTBCity.json'


class AlfaStatusLeadTestCase(TestCase):
    def setUp(self) -> None:
        import datetime as DT
        from_dt = DT.datetime.fromisoformat('2022-06-21')
        from_dt = from_dt.timestamp()
        print(int(from_dt))

        to_dt = DT.datetime.fromisoformat('2022-06-22')
        to_dt = to_dt.timestamp()
        print(int(to_dt))
        self.json_all = {
            'pageNumber': 0,
            'perPage': 100,
            'fromDate': f'{int(from_dt)}000',
            'toDate': f'{int(to_dt)}000',
        }
        self.json_solo_lead = '6c8df76d-c0f3-4d69-b323-941fd0e39eda'
        self.obj = AlfaStatusLead(self.json_all, False)

    def test_get_date(self):
        import datetime as DT
        dt = DT.datetime.fromisoformat('2022-06-05')
        print(int(dt.timestamp()))

    def test_get_rezult(self):
        test_res = self.obj.get_rezult()
        pprint(test_res)


class AlfaScoringTestCaset(TestCase):
    def setUp(self) -> None:
        self.key = os.environ.get('alfabank_dict_key')
        self.json = {
            'organizationInfo': {'inn': '6685003097'},
            "contactInfo": [{"phoneNumber": '79600417480'}],
            "productInfo": [{"productCode": "LP_RKO"}]
        }

    def test_headers_test_false(self):
        obj = AlfaScoring(self.json, False)
        obj.get_response_functions()
        self.assertEqual(obj.args_request['headers']['API-key'], self.key)

    def test_headers_test_true(self):
        obj = AlfaScoring(self.json, True)
        obj.get_response_functions()
        self.assertEqual(obj.args_request['headers']['API-key'], 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')

    def test_get_rezult_false(self):
        obj = AlfaScoring(self.json, False)
        obj.get_rezult()
        self.assertEqual(obj.success, True)
        print(obj.response)
        self.assertIn(obj.rezult, ['Свободен', 'Занят'])

    def test_get_rezult_true(self):
        obj = AlfaScoring(self.json, True)
        obj.get_rezult()
        self.assertEqual(obj.success, True)
        self.assertIn(obj.rezult, ['Свободен', 'Занят'])


class AlfaLeadTestCase(TestCase):
    def setUp(self):
        self.key = os.environ.get('alfabank_dict_key')
        self.json = {
            'organizationInfo': {
                'organizationName': 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ВЕЛ-ТОРГ"',
                'inn': '9725074920',
            },
            'contactInfo': [{
                "fullName": 'РОМАНОВ НИКОЛАЙ ВАСИЛЬЕВИЧ',
                "phoneNumber": '79771036772',
            }
            ],
            "requestInfo": {
                "comment": '',
                "cityCode": '9fdcc25f-a3d0-4f28-8b61-40648d099065'
            },
            "productInfo": [{"productCode": "LP_RKO"}]
        }

    def test_get_response(self):
        obj = AlfaLead(self.json, True)

        self.assertIsInstance(obj.get_guarantee_response(), Response)

    # def test_headers_test_false(self):
    #     obj = AlfaLead(self.json, False)
    #     obj.get_response_functions()
    #     self.assertEqual(obj.args_request['headers']['API-key'], self.key)

    def test_headers_test_true(self):
        obj = AlfaLead(self.json, True)
        obj.get_response_functions()
        self.assertEqual(obj.args_request['headers']['API-key'], 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa')

    def test_get_rezult(self):
        obj = AlfaLead(self.json, True)
        obj.get_rezult()
        self.assertEqual(obj.success, True)
        print(obj.rezult)
        self.assertRegex(obj.rezult,
                         r'^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}')

    def test_do_json_UNACCEPTABLE_COMPANY(self):
        obj = AlfaLead(self.json, True)
        obj.response_json = {'errors': [
            {'status': 403, 'code': 'UNACCEPTABLE_COMPANY', 'title': 'Unacceptable company',
             'detail': 'Unfortunately, the Bank cannot accept the company with the provided TIN [5907052137].'}]}
        self.assertRegex(obj.do_json(), r'^Клиент занят другими$')

    def test_do_json_LEADS_LIMIT_ERROR(self):
        obj = AlfaLead(self.json, True)
        obj.response_json = {'errors': [
            {'status': 403, 'code': 'LEADS_LIMIT_ERROR', 'title': 'Leads limit exceeded',
             'detail': 'The allowed limit of 45 leads has already exceeded.'}]}
        self.assertRegex(obj.do_json(), r'^Превышен лимит$')

    def test_do_json_validationError(self):
        obj = AlfaLead(self.json, True)
        obj.response_json = {'errors': [{'status': 400, 'code': 'validationError',
                                         'detail': 'Значение 79099096723986 поля $.contactInfo[*].phoneNumber не соответствует регулярному выражению 7\\d{10}',
                                         'title': 'Ошибка обработки данных', 'meta': {
                'jexceptionMsg': 'javax.validation.ValidationException: Значение 79099096723986 поля $.contactInfo[*].phoneNumber не соответствует регулярному выражению 7\\d{10}'}}]}
        self.assertRegex(obj.do_json(), r'не соответствует регулярному выражению')


class VTBStatusLeadTestCase(TestCase):
    def setUp(self) -> None:
        json = {'leadid': 8499234}
        self.obj = VTBStatusLead(json)

    def test_get_rezult(self):
        print(self.obj.get_rezult())
        print(self.obj.response.text)


class VTBScoringTestCase(TestCase):
    def setUp(self):
        self.json = {
            "leads": [{"inn": "9721194775", "productCode": "Payments"}, {"inn": "780448824307", "productCode": "Payments"}, {"inn": "540317272444", "productCode": "Payments"}, {"inn": "661908324831", "productCode": "Payments"}, {"inn": "665800616459", "productCode": "Payments"}, {"inn": "665802770417", "productCode": "Payments"}]
        }

    # def test_test(self):
    #     obj = VTBScoring(self.json)  #
    #     obj.get_rezult()
    #     content = b'{"leads":[{"inn":"6679151716","productCode":"Payments","responseCode":"POSITIVE","responseCodeDescription":"\xd0\x9b\xd0\xb8\xd0\xb4 \xd0\xbc\xd0\xbe\xd0\xb6\xd0\xb5\xd1\x82 \xd0\xb1\xd1\x8b\xd1\x82\xd1\x8c \xd0\xb2\xd0\xb7\xd1\x8f\xd1\x82 \xd0\xb2 \xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd1\x83"},{"inn":"4400008354","productCode":"Payments","responseCode":"POSITIVE","responseCodeDescription":"\xd0\x9b\xd0\xb8\xd0\xb4 \xd0\xbc\xd0\xbe\xd0\xb6\xd0\xb5\xd1\x82 \xd0\xb1\xd1\x8b\xd1\x82\xd1\x8c \xd0\xb2\xd0\xb7\xd1\x8f\xd1\x82 \xd0\xb2 \xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd1\x83"}]}'
    #     cont = content.decode()
    #     print(cont)
    #     print(json.loads(cont))
        # j = "{'leads': [{'inn': '4400008354', 'productCode': 'Payments', 'responseCode': 'POSITIVE', 'responseCodeDescription': 'Лид может быть взят в работу'}, {'inn': '6679151716', 'productCode': 'Payments', 'responseCode': 'POSITIVE', 'responseCodeDescription': 'Лид может быть взят в работу'}]}"
        # print()
        # print(json.loads(j))
        # test_res = json.loads()
        # print(test_res)
        # print(type(test_res))

    def test_get_rezult(self):
        obj = VTBScoring(self.json)
        print(obj.get_rezult())
        # print(obj.exist_error_authorization())

        print(obj.response.content)
        print(obj.response.status_code)
        print(obj.args_request)
        self.assertEqual(obj.success, True)
        self.assertEqual(sorted([dict_client['inn'] for dict_client in obj.rezult]),
                         sorted([json['inn'] for json in self.json['leads']]))

    def test_do_json_unauthorized(self):
        obj = VTBScoring(self.json)
        obj.response_json = {'httpCode': '401', 'httpMessage': 'Unauthorized',
                             'moreInformation': "<BackErr> needConfirm"}
        print(obj.do_json())
        self.assertEqual(obj.success, True)
        self.assertEqual(sorted([dict_client['inn'] for dict_client in obj.rezult]),
                         sorted([json['inn'] for json in self.json['leads']]))

    def test_do_json_needConfirm(self):
        obj = VTBScoring(self.json)
        print(obj.__dict__)
        obj.response_json = {'status': 'needConfirm'}
        obj.do_json()
        print(obj.rezult)
        self.assertEqual(obj.success, True)
        self.assertEqual(sorted([dict_client['inn'] for dict_client in obj.rezult]),
                         sorted([json['inn'] for json in self.json['leads']]))


class VTBLeadTestCase(TestCase):
    def setUp(self):
        self.json = {
            "leads": [
                {
                    "phone": "+79525798581",
                    "consentOnPersonalDataProcessing": True,
                    "inn": "6162088338",
                    "city": "Каменск-Шахтинский",
                    "productCode": "Payments",
                    "sourceLeadId": "707463271",
                    "companyName": 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "АРАКС"'
                },
                # {
                #     "phone": "+7123456789",
                #     "consentOnPersonalDataProcessing": True,
                #     "inn": "547779835982",
                #     "city": "Москва",
                #     "productCode": "Payments",
                #     "sourceLeadId": "01",
                # }
            ]
        }

    def test_get_rezult(self):
        obj = VTBLead(self.json)
        obj.custom_test = False
        obj.get_rezult()
        print(obj.rezult)
        self.assertEqual(obj.success, True)
        self.assertEqual(sorted([dict_client['sourceLeadId'] for dict_client in obj.rezult]),
                         sorted([json['sourceLeadId'] for json in self.json['leads']]))

    def test_bad_request(self):
        obj = VTBLead(self.json, True)
        obj.custom_test = True

        def get_response():
            return return_test_response({'httpCode': '400', 'httpMessage': 'Bad request',
                                         'moreInformation': 'Internal Server Error: Validate: Internal Validation Error'},
                                        200)

        obj.return_test_response = get_response
        self.assertEqual(obj.get_rezult(), {'httpCode': '400', 'httpMessage': 'Bad request',
                                            'moreInformation': 'Internal Server Error: Validate: Internal Validation Error'})
        self.assertEqual(obj.success, False)

    def test_do_status_code(self):
        def get_response():
            from requests.models import Response
            the_response = Response()
            the_response.status_code = 400
            return the_response

        obj = VTBLead(self.json, True)
        obj.custom_test = True

        obj.return_test_response = get_response
        self.assertEqual(obj.get_rezult(), 400)
        self.assertEqual(obj.success, False)


    def test_0(self):
        '''Отправка заявки на настоящий сервер'''

        # [{'responseCode': 'CITY_NOT_AVAILABLE', 'responseCodeDescription': "Ошибка в поле 'city': Выбранный город недоступен для создания заявки. Для уточнения информации обратитесь к своему персональному менеджеру.."}]

        obj = VTBLead(self.json, False)
        print(obj.get_rezult())
        print(obj.response_json)
        print(obj.response.status_code)
        print(obj.success)
        print(obj.resend_send)




class TochkaStatusLeadTestCase(TestCase):
    def setUp(self) -> None:
        workMode = 1
        json = {
            "token": '',
            "request": {
                'from': f'2022-05-24',
                'days': f'10',
            },
            'workMode': f"{workMode}"
        }
        self.obj = TochkaStatusLead(json)

    def test_get_rezult(self):
        test_res = self.obj.get_rezult()
        print(test_res)
        return True


class TochkaLeadTestCase(TestCase):
    def setUp(self):
        self.json = {
            "token": '',
            "request": {
                'inn': '9725074920',
                'name': "ООО 'ВЕЛ-ТОРГ'",
                'last_name': 'Романов',
                'first_name': 'Николай',
                "second_name": "ОТЧЕСТВО",
                'telephone': f'+79527001328',
                'comment': '',
                'address': ''
            },
            'workMode': '0'
        }

    def test_get_rezult(self):
        obj = TochkaLead(self.json)
        obj.get_rezult()
        self.assertEqual(obj.success, True)
        self.assertRegex(str(obj.rezult), r'^[0-9]{5}$|^Передан неверный ИНН.$|^Ошибка: заявка с ИНН')

    def test_0(self):
        obj = TochkaLead(self.json)

        print(obj.get_rezult())
        print(obj.response_json)

class TestTochkaLeedRef(TestCase):
    def setUp(self) -> None:
        '''
        formservices[]:
        c1dbed398635e5729a7f32d17aeb88de
        phone:
        +7 (994) 333-5632
        advid:
        yandex_uid:
        page_description:
        Заявку оставили за клиента сотрудники партнёра. Обычное предложение РКО.
        page_url:
        inn:
        454545454545
        comment:
        ТЕСТОВАЯ ЗАЯВКА
        crm_type:
        signup
        gclid:
        form-spec-comments:
        tildaspec-cookie:
        tochka_analytics_client_uid=5a437c8c-9b58-d0c6-3303-812b9419a6a1; _gcl_au=1.1.2063294800.1667818077; _ga=GA1.3.1566587440.1667818078; _gid=GA1.3.2034256149.1667818078; tmr_lvid=a8283bfeca8bce5f725136cc83c6a781; tmr_lvidTS=1667818077915; _ym_uid=1667818078419560326; _ym_d=1667818078; _gid=GA1.2.2034256149.1667818078; tildauid=1667818079508.335243; _ga_4R46N8WCLZ=GS1.1.1667966449.7.0.1667966449.60.0.0; _ga=GA1.2.1566587440.1667818078; tildasid=1667966450769.883627; _ym_isad=2; _ym_visorc=w; previousUrl=partner.tochka.com%2Ffp%2F; tmr_detect=0%7C1667966452674; tmr_reqNum=19
        tildaspec-referer:
        https://partner.tochka.com/fp/?referer1=kckireev
        tildaspec-formid:
        form305838800
        tildaspec-formskey:
        8e01b006ad02c72decfea4d870db663d
        tildaspec-version-lib:
        02.001
        tildaspec-pageid:
        7007880
        tildaspec-projectid:
        650828
        tildaspec-lang:
        RU
        tildaspec-fp:
        6354646d386863386c72752d52552c72752c656e2d55532c656e7057696e333276476f6f676c6520496e632e614d6f7a696c6c616e4e65747363617065706c696e7465726e616c2d7064662d766965776572696e7465726e616c2d7064662d766965776572696e7465726e616c2d7064662d766965776572696e7465726e616c2d7064662d766965776572696e7465726e616c2d7064662d766965776572707231773130373868393639
        tildaspec-tildacaptcha:
        03AEkXODADaatSHzMCn18p595NX_J-fO6IDhlBp7jJK33vn1JgZDq0TXe8NwQ5CrI8yO-dpESagHTJQGVGc6HVGewT4PVfj1gsRn6TST14m1-Z7FWRuHnA7zJ2lE-4yMCNxqXP8KzYpOHTCJhJRGtmVAStYR-_kEO92FTkSV78CBr8a6QbF7zd-0BYiXla2g8o93I14uL12uEeHGBby7Dx_FPYEBlbZEet0iNFnflEqh_XrDONbApvixHuvSQ4RuOx7M9NgooGRzfHX11NOmeG6d0yEO3LcPKok1K2AQhYyPpd_T79SajdrtMO5rmcE8KDzHue2_oh4Its5pkoWAGh31iDnfBvt_z5r3-Lso7fTcN-56zdML2rZIughCMTdoq1RhTCpzLZaXfFoB-25rqFMsQnX-JdWlUx3JnzN_4ym_3AhB3ODkGmg-A3Yf_YpnWkN8IBGLiiG_4mz9rjort80BkiVtBRF18dETuJadWBMUMuuR2pLqVKsroHmdDpl4iBd2h2IpEuaibq
        :return:
        6324117881
        '''

        self.json = {
                'formservices[]': 'c1dbed398635e5729a7f32d17aeb88de',
                'phone': '+7 (927) 571-4003',
                'advid': 'kckireev',
                'page_description': 'Заявку оставили за клиента сотрудники партнёра. Обычное предложение РКО.',

                'yandex_uid': '',

                'page_url': 'partner.tochka.com/fp/',

                'inn': '3000003670',
                'comment': 'ТЕСТОВАЯ ЗАЯВКА',
                'crm_type': 'signup',
                'gclid': '',
                'form-spec-comments': '',
                'tildaspec-cookie': 'tochka_analytics_client_uid=5a437c8c-9b58-d0c6-3303-812b9419a6a1; _gcl_au=1.1.2063294800.1667818077; _ga=GA1.3.1566587440.1667818078; tmr_lvid=a8283bfeca8bce5f725136cc83c6a781; tmr_lvidTS=1667818077915; _ym_uid=1667818078419560326; _ym_d=1667818078; tildauid=1667818079508.335243; _gid=GA1.2.1566780950.1668577339; _gid=GA1.3.1566780950.1668577339; tildasid=1668658597858.489091; _ym_visorc=w; _ym_isad=2; _ga_4R46N8WCLZ=GS1.1.1668658601.15.1.1668659581.56.0.0; _ga=GA1.1.1566587440.1667818078; tmr_detect=0%7C1668659582864; previousUrl=partner.tochka.com%2Ffp%2F; tmr_reqNum=80',
                'tildaspec-referer': 'https://partner.tochka.com/fp/?referer1=kckireev',

                'tildaspec-formid': 'form305838800',
                'tildaspec-formskey': '8e01b006ad02c72decfea4d870db663d',
                'tildaspec-version-lib': '02.001',
                'tildaspec-pageid': 7007880,
                'tildaspec-projectid': 650828,
                'tildaspec-lang': 'RU',
                'tildaspec-fp': '6354646d386863386c72752d52552c72752c656e2d55532c656e7057696e333276476f6f676c6520496e632e614d6f7a696c6c616e4e65747363617065706c696e7465726e616c2d7064662d766965776572696e7465726e616c2d7064662d766965776572696e7465726e616c2d7064662d766965776572696e7465726e616c2d7064662d766965776572696e7465726e616c2d7064662d7669657765727072317737373468393639',
                # 'tildaspec-tildacaptcha':'03AEkXODBHDYw9bNPm8gxZ0sMhGNG94t-G8JSH_lM4HHPYqMifTxo8SiQWCoORIcF2iNyZrfUuYV-RhNW6f0t4Th5BgHOZMHTdIJGjY3QMML42jm3xL4VP-4Ygq7qtgIduuElzoU0fl6g5OlPBsFTxa_MoWH1sWlBgupaWgFDa00bhT9a-mw6u40DspOed-xf2FBnnCsSmNIzYxVZ-Bq_uplc6ECspK_AmWRAGrA8dtsgxUKRgjPSU1h3kPgwfOlizAVPvgXFY7CVFMtl-Id_dpnirnY7jEMdGb_zz3_TfJ6iDf91ywBXT_rbdDiMOi3SLneqkwDoj-xG1rQWl2pEwWO3UQ0b0EfKriFqRH2bnTNua6VGfHu7b2WxRrQstzmf1cpiPleSseqwob9abDQWFZpkzq7Ng7P7-YkOJLc-F4Vz5e6ucPQqO9jWIuqcB9RNe07PH-CmkZhWVJNekNBqZWbQzulm-XB4hUX9aZUaBavQN9sPbhYO_-C3FNtQLVn-4_vDnbY822MwXIvMzH61zLDfqYND71exX5Q',



                }


    def test_get_rezult(self):
        self.obj = TochkaLeedRef(self.json)
        print(self.obj.get_rezult())
        print(self.obj.response_json)
        print(self.obj.response.request.headers)

    def test_0(self):
        print(get_recaptcha_v2('47.241.165.133:443'))

    def test_1(self):
        proxies_list = ["154.26.134.214:80", "154.26.134.217:80", "47.241.165.133:443", "15.235.150.136:80", "47.74.152.29:8888",
         "174.138.24.67:8080", "112.140.186.124:808", "118.107.44.181:80", "118.107.44.181:8000", "45.12.31.35:80",
         "45.14.174.110:80", "141.101.120.156:80", "172.67.208.171:80", "23.227.38.11:80", "203.34.28.8:80",
         "203.22.223.136:80", "203.30.191.227:80", "185.162.229.41:80", "185.162.231.6:80", "203.23.106.75:80",
         "203.23.103.12:80", "45.8.107.166:80", "203.28.9.225:80", "203.23.103.57:80", "203.24.108.96:80",
         "203.13.32.213:80", "185.162.231.163:80", "45.8.106.205:80", "203.24.109.184:80", "203.28.9.118:80",
         "185.162.229.171:80", "203.13.32.137:80", "45.12.30.121:80", "45.8.106.110:80", "203.13.32.72:80",
         "185.162.228.83:80", "203.30.190.49:80", "203.34.28.245:80", "203.28.9.201:80", "203.32.120.98:80",
         "203.24.109.181:80", "45.14.174.63:80", "203.32.120.153:80", "203.13.32.63:80", "45.8.107.143:80",
         "185.162.229.237:80", "141.193.213.179:80", "172.67.185.188:80", "185.238.228.171:80", "185.238.228.144:80",
         "172.67.55.32:80", "141.101.121.44:80", "141.101.121.12:80", "141.101.122.64:80", "141.101.122.111:80",
         "172.67.165.253:80", "172.67.253.207:80", "172.67.70.50:80", "172.67.23.197:80", "172.67.180.8:80",
         "45.12.31.190:80", "203.24.109.202:80", "203.13.32.166:80", "45.8.107.49:80"]


        print(len(proxies_list))
        for proxy in proxies_list:
            ob = TochkaLeedRef(self.json, proxy).get_obj_rezult()
            print(f"{ob.rezult} == {proxy}")
        #     if ob.success:
        #         print(f'{proxy} - рабочий')
        #         break


    def test_2(self):
        proxy = '47.241.165.133:443'
        ob = TochkaLeedRef(self.json, proxy).get_obj_rezult()
        print(ob.rezult)


class TochkaRegistryUrTestCase(TestCase):
    def setUp(self) -> None:
        self.json = {
            "token": '',
            "request": {
                'snils': '083-367-324-77',
                'org_form': 'ltd',
                'inn': '9725074920',
                'last_name': 'Романов',
                'first_name': 'Николай',
                'birthday': '2000-02-02',
                'telephone': f'+79527001328',
                'dateStart': '2018-02-12',
                'typeDoc': '21',
                'number': '654321',
                'serial': '7517'
            },
            'workMode': '0'
        }

        self.obj = TochkaRegistryUr(self.json)

    def test_get_rezult(self):
        self.obj.get_rezult()
        print(self.obj.rezult)


class TochkaAddDocsTestCase(TestCase):
    def setUp(self) -> None:
        self.json = {
            "token": '4irzv9dzkmm5yya3pz6gslb3rjsv90gj',
            "request": {
                'code': '9725074920',
                'zip': 'C:\\spreadsheets_srm\\uploads\\docs\\admin'
            },
            'workMode': '0'
        }
        self.obj = TochkaAddDocs(self.json)

    def test_pack_docs(self):
        print(self.obj.json)

    def test_get_rezult(self):
        self.obj.get_rezult()
        print(self.obj.rezult)


class ModuleLeadTestCase(TestCase):
    def setUp(self) -> None:
        self.json = {
            "inn": "591400258078",
            "ogrn": "322554300031948",
            "person_email": "nan@mail.ru",
            "person_firstname": "Имя",
            "person_surname": "Фамилия",
            "person_middlename": "Отчество",
            "person_phone": "79000000000",
            "comment": "",
            "stg": [
                "ACCOPEN"
            ],
            "company_name": "ИП Фамилия Имя Отчество"
        }

    def test_base_url_test(self):
        obj = ModuleLead(self.json, True)
        obj.custom_test = True
        obj.get_response_functions()
        self.assertEqual(
            obj.args_request['url'],
            f'https://partnertest.modulbank.ru/public/agent/app/add?tnx={os.environ.get("module_tnx")}'
        )

    def test_base_url(self):
        obj = ModuleLead(self.json, True)
        obj.custom_test = False
        obj.get_response_functions()
        self.assertEqual(
            obj.args_request['url'],
            f'https://partnertest.modulbank.ru/public/agent/app/add?tnx={os.environ.get("module_tnx")}'
        )

    def test_get_rezult_custom_test_true(self):
        obj = ModuleLead(self.json, True)
        obj.custom_test = True
        obj.get_rezult()
        print(obj.rezult)
        self.assertEqual(obj.success, True)
        self.assertRegex(obj.rezult,
                         r'^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}')

    # def test_get_rezult_custom_test_false(self):
    #     obj = ModuleLead(self.json, True)
    #     obj.custom_test = False
    #     obj.get_rezult()
    #     self.assertEqual(obj.success, True)
    #     self.assertRegex(obj.rezult,
    #                      r'^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}')

    def test_do_json(self):
        json = {
            "inn": "383702760141",
            "ogrn": "322030000020615",
            "person_email": "nan@mail.ru",
            "person_firstname": "ЕЛЕНА",
            "person_surname": "ВАНЧИКОВА",
            "person_middlename": "АЛЕКСАНДРОВНА",
            "person_phone": "79384965043",
            "comment": "",
            "stg": [
                "ACCOPEN"
            ],
            "company_name": "ИП ВАНЧИКОВА ЕЛЕНА АЛЕКСАНДРОВНА"
        }
        obj = ModuleLead(json, True)
        obj.response_json = {'status': 'ok', 'response': {'page': 1, 'pageSize': 15, 'total': 78, 'list': [

            {'id': 'CF2D5672-16DF-408A-9BD9-CE2613D8E05A', 'num': 671359, 'dadd': '2021-10-13T19:30:10.903',
             'state': 'success', 'lastUpd': '2021-10-15T18:05:00.373', 'stg': ['ACCOPEN'], 'inn': '7713485142',
             'client_name': 'ООО "СИБРИЗ"', 'person_phone': '79153632139', '__num_searchable': '671359'},
            {'id': '848B89C1-498D-4944-9B89-F19C7408D32A', 'num': 664406, 'dadd': '2021-10-11T16:21:59.15',
             'state': 'success', 'lastUpd': '2021-10-13T19:04:53.587', 'stg': ['ACCOPEN'], 'inn': '9723126097',
             'client_name': 'ООО "ПРИМА"', 'person_phone': '79851462972', '__num_searchable': '664406'},
            {'id': '05881C15-7EE9-4EF1-A5A5-39010DE49D46', 'num': 662579, 'dadd': '2021-10-11T00:09:49.093',
             'state': 'decline.double', 'lastUpd': '2021-10-11T00:10:00.277', 'stg': ['ACCOPEN'], 'inn': '9704091265',
             'client_name': 'ООО "ГЕРМЕС"', 'person_phone': '79151352742', '__num_searchable': '662579'},
            {'id': 'F4E3F811-0160-4487-AFD5-B0285241A52B', 'num': 662578, 'dadd': '2021-10-11T00:06:37.47',
             'state': 'waitformeeting', 'lastUpd': '2022-04-26T20:53:04.157', 'stg': ['ACCOPEN'], 'inn': '7726484266',
             'client_name': 'ООО "СМУ"', 'person_phone': '79151352686', '__num_searchable': '662578'},
            {'id': '9D0A9185-2F8B-4BBE-87E3-5729C1013D88', 'num': 662576, 'dadd': '2021-10-11T00:01:19.867',
             'state': 'decline.double', 'lastUpd': '2021-10-11T00:05:00.433', 'stg': ['ACCOPEN'], 'inn': '262517148226',
             'client_name': 'ИП СОЩЕНКО АЛЕКСЕЙ ВЛАДИМИРОВИЧ', 'person_phone': '79153635015',
             '__num_searchable': '662576'},
            {'id': '75216E9F-6200-4FF6-92FE-54B3CE189A7E', 'num': 650883, 'dadd': '2021-10-06T14:43:03.7',
             'state': 'success', 'lastUpd': '2021-10-08T20:03:48.6', 'stg': ['ACCOPEN'], 'inn': '330646707810',
             'client_name': 'Индивидуальный предприниматель Гафаров Рамиз Ниязали Оглы', 'person_phone': '79151360842',
             '__num_searchable': '650883'},
            {'id': '8FF57C80-19D2-4E9F-AEB1-053F0F948E56', 'num': 646306, 'dadd': '2021-10-04T23:19:13.58',
             'state': 'decline.double', 'lastUpd': '2021-10-04T23:20:00.497', 'stg': ['ACCOPEN'], 'inn': '9704090896',
             'client_name': 'ООО "ПЛАЗА"', 'person_phone': '79851463060', '__num_searchable': '646306'},
            {'id': 'D2CDE4C9-271B-41F1-979B-35A5782B6B64', 'num': 1738110, 'dadd': '2022-05-25T13:10:03.013',
             'state': 'init', 'lastUpd': '2022-05-25T13:10:03.013', 'stg': ['ACCOPEN'], 'inn': '383702760141',
             'client_name': 'ИП ВАНЧИКОВА ЕЛЕНА АЛЕКСАНДРОВНА', 'person_phone': '79384965043',
             '__num_searchable': '1738110'},
            {'id': 'BA3A89BD-EECE-4AE5-A3A7-067EFB41DC36', 'num': 646288, 'dadd': '2021-10-04T23:13:12.113',
             'state': 'decline.double', 'lastUpd': '2021-10-04T23:15:00.48', 'stg': ['ACCOPEN'], 'inn': '9703050523',
             'client_name': 'ООО "ДЕЛЬТА"', 'person_phone': '79851462894', '__num_searchable': '646288'},
            {'id': '7B563227-3115-4ACC-9BA4-2A14A73DE40D', 'num': 646285, 'dadd': '2021-10-04T23:11:49.903',
             'state': 'decline.double', 'lastUpd': '2021-10-04T23:15:00.48', 'stg': ['ACCOPEN'], 'inn': '771573339751',
             'client_name': 'ИП ШЕСТАКОВ СЕРГЕЙ НИКОЛАЕВИЧ', 'person_phone': '79851460848',
             '__num_searchable': '646285'},
            {'id': 'E344DC95-9A95-4862-B6CA-74B785747E8E', 'num': 643485, 'dadd': '2021-10-03T13:15:26.03',
             'state': 'success', 'lastUpd': '2021-10-07T13:04:17.42', 'stg': ['ACCOPEN'], 'inn': '9704090617',
             'client_name': 'ООО "АВС"', 'person_phone': '79850875811', '__num_searchable': '643485'},
            {'id': 'DA004D55-A43A-4051-9490-C402607BC7BF', 'num': 643484, 'dadd': '2021-10-03T13:13:17.51',
             'state': 'success', 'lastUpd': '2021-10-07T13:04:17.42', 'stg': ['ACCOPEN'], 'inn': '052999963528',
             'client_name': 'Индивидуальный предприниматель Мисриханова Жанета Рамазановна',
             'person_phone': '79153632139', '__num_searchable': '643484'},
            {'id': '42A654DF-3D76-4686-B8BE-0D1C0AEC5F6A', 'num': 643483, 'dadd': '2021-10-03T13:05:36.607',
             'state': 'success', 'lastUpd': '2021-10-06T20:33:48.473', 'stg': ['ACCOPEN'], 'inn': '9723124646',
             'client_name': 'ООО "ЗУМ"', 'person_phone': '79851465477', '__num_searchable': '643483'},
            {'id': '8410040F-7E2D-4B36-81A8-E9A76B40E85E', 'num': 643481, 'dadd': '2021-10-03T13:03:41.653',
             'state': 'decline.double', 'lastUpd': '2021-10-03T13:05:00.923', 'stg': ['ACCOPEN'], 'inn': '9703049408',
             'client_name': 'ООО "МАКСИМУМ"', 'person_phone': '79166529856', '__num_searchable': '643481'},
            {'id': '5E9ADBEE-69D5-4398-B3DA-8191EE96A8D8', 'num': 643479, 'dadd': '2021-10-03T13:01:11.41',
             'state': 'success', 'lastUpd': '2021-10-06T20:33:48.473', 'stg': ['ACCOPEN'], 'inn': '343520598450',
             'client_name': 'Индивидуальный предприниматель Рзаева Махбуба Амрага Кызы', 'person_phone': '79153631180',
             '__num_searchable': '643479'}]}, '_requestid': 'A066BDD7-3C61-EE47-0B43-FB1C411E1C04',
                             'access': [{'obj': 'agent.alerts.clear'}, {'obj': 'agent.alerts.delete'},
                                        {'obj': 'agent.alerts.get'},
                                        {'obj': 'agent.app.add'}, {'obj': 'agent.app.get'},
                                        {'obj': 'agent.app.get_status'},
                                        {'obj': 'agent.app.list'}, {'obj': 'agent.background.refresh'},
                                        {'obj': 'agent.employee.acl'},
                                        {'obj': 'agent.employee.add'}, {'obj': 'agent.employee.list'},
                                        {'obj': 'agent.employee.remove'},
                                        {'obj': 'agent.file.add'}, {'obj': 'agent.file.delete'},
                                        {'obj': 'agent.file.send'},
                                        {'obj': 'agent.misc.search_bic'}, {'obj': 'agent.misc.search_company'},
                                        {'obj': 'agent.profile.get'}, {'obj': 'agent.profile.update'},
                                        {'obj': 'agent.subpartner.invite'},
                                        {'obj': 'agent.subpartner.link'}, {'obj': 'agent.subpartner.list'},
                                        {'obj': 'billing.balance.get'},
                                        {'obj': 'billing.payments.demand'}, {'obj': 'billing.payments.list'},
                                        {'obj': 'billing.payments.payout_transactions'},
                                        {'obj': 'users.account.changelogin'},
                                        {'obj': 'users.account.changepass'}, {'obj': 'users.account.logout'}]}

        print(obj.do_json())


class MoeDeloLeadTestCase(TestCase):
    def setUp(self) -> None:
        self.json = {
            "Fio": "САЛЬНИКОВ АЛЕКСАНДР НИКОЛАЕВИЧ",
            "Email": "4018994@mail.ru",
            "Phone": "+7 (917) 401-89-94",
            "Inn": "2301109140",
            "Product": "Accounting",
            "UtmSource": "partner.1326.BIZ",
            "UtmCampaign": "partner_10693496",
            "Comment": "Тестовая заявка"
        }

        self.obj = MoeDeloLead(self.json)

    def test_get_rezult_custom_test_true(self):
        obj = MoeDeloLead(self.json, True)
        obj.custom_test = True
        obj.get_rezult()

        self.assertEqual(obj.success, True)
        self.assertRegex(obj.rezult, r'^[0-9]{3}-[0-9]{3}-[0-9]{3}$')

    def test_get_rezult_custom_test_false(self):
        obj = MoeDeloLead(self.json, False)
        obj.custom_test = False
        print(obj.get_rezult())
        print(obj.response.content)
        print(obj.success)
        # self.assertEqual(obj.success, True)
        # self.assertRegex(obj.rezult, r'^[0-9]{2}[0-9]{3}[0-9]{3}$')

    def test_headers_test_true(self):
        obj = MoeDeloLead(self.json, True)
        obj.get_response_functions()
        self.assertRegex(obj.args_request['headers']['X-WSSE'], r'^UsernameToken|PasswordDigest')


class OpenStatusLeadTestCase(TestCase):
    def setUp(self) -> None:
        json = {'id': '597cf7b3-072a-49e2-aae0-f57c91b783a1'}
        self.obj = OpenStatusLead(json, True)

    def test_get_result(self):
        test_res = self.obj.get_rezult()
        print(test_res)


class OpenScoringTestCase(TestCase):
    def setUp(self) -> None:
        self.inns = ['9704122315', '9704122347']
        self.json = {"inns": self.inns}

    # def test_get_rezult_test_true(self):
    #     obj = OpenScoring(self.json, True)
    #     print(obj.get_rezult())
    #     self.assertEqual(obj.success, True)
    #     self.assertEqual(sorted([dict_client['inn'] for dict_client in obj.rezult]),
    #                      sorted([json for json in self.json['inns']]))


class OpenScoringIDTestCase(TestCase):
    def setUp(self) -> None:
        self.inns = ['9704122315', '9704122347']
        self.json = {"inns": self.inns}

    # def test_get_rezult_custom_test_true(self):
    #     obj = OpenScoringID(self.json, True)
    #     obj.custom_test = True
    #     obj.get_rezult()
    #     self.assertEqual(obj.success, True)
    #     self.assertRegex(
    #         obj.rezult,
    #         r'^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}'
    #     )

    # def test_get_rezult_custom_test_false(self):
    #     obj = OpenScoringID(self.json, True)
    #     obj.custom_test = False
    #     obj.get_rezult()
    #     self.assertEqual(obj.success, True)
    #     self.assertRegex(
    #         obj.rezult,
    #         r'^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}'
    #     )

    def test_base_url_test(self):
        obj = OpenScoringID(self.json, True)
        obj.get_response_functions()
        self.assertEqual(obj.args_request['url'], 'https://openpartners.ru/api/v2/request/getduplicates/test')

    def test_base_url(self):
        obj = OpenScoringID(self.json, False)
        obj.get_response_functions()
        self.assertEqual(obj.args_request['url'], 'https://openpartners.ru/api/v2/request/getduplicates')


class OpenScoringStatusTestCase(TestCase):
    def setUp(self) -> None:
        OpenScoringStatus.custom_test = True
        inns = ['9704122315', '9704122347']
        open_scoring_id_json = {"inns": inns}
        obj = OpenScoringID(open_scoring_id_json, True)
        obj.custom_test = False
        self.json = {'id': obj.get_rezult()}

    def test_base_url_test(self):
        obj = OpenScoringStatus(self.json, True)
        obj.get_response_functions()
        self.assertEqual(
            obj.args_request['url'],
            'https://openpartners.ru/api/v2/request/getduplicates/test'
        )

    def test_base_url(self):
        obj = OpenScoringStatus(self.json, False)
        obj.get_response_functions()
        self.assertEqual(
            obj.args_request['url'],
            'https://openpartners.ru/api/v2/request/getduplicates'
        )

    # def test_id_custom_test_true(self):
    #     obj = OpenScoringStatus(self.json, True)
    #     obj.custom_test = True
    #     obj.get_rezult()
    #     print(obj.rezult)
    #     self.assertEqual(obj.success, True)
    #     self.assertEqual(obj.response_json['id'], self.json['id'])

    # def test_id_custom_test_false(self):
    #     obj = OpenScoringStatus(self.json, True)
    #     obj.custom_test = False
    #     obj.get_rezult()
    #     self.assertEqual(obj.success, True)
    #     self.assertEqual(obj.response_json['id'], self.json['id'])

    def test_get_rezult(self):
        obj = OpenScoringStatus(self.json, True)
        obj.custom_test = False

        print(obj.get_rezult())
        print(obj.args_request)
        print(obj.response.text)


class OpenLeadTestCase(TestCase):
    def setUp(self) -> None:
        self.json = {
            'full_name': 'Иванов Петр Иванович',
            'inn': '688153834076',
            'phone': '+79771036772',
            'email': 'abc5462t@mail.ru',
            'city': "Москва",
            'comment': '',
        }

    def test_init(self):
        obj = OpenLead(self.json, True)
        obj.custom_test = False
        obj.get_response_functions()
        print(obj.args_request)

    def test_get_response_custom_test_false(self):
        obj = OpenLead(self.json, True)
        obj.custom_test = False
        obj.get_response_functions()
        self.assertEqual(obj.args_request['url'], 'https://openpartners.ru/api/v2/request/add/test')

    def test_get_response_custom_test_true(self):
        obj = OpenLead(self.json, True)
        obj.custom_test = True
        obj.get_response_functions()
        self.assertEqual(obj.args_request['url'], 'https://openpartners.ru/api/v2/request/add/test')

    def test_get_rezult_custom_test_true(self):
        obj = OpenLead(self.json, True)
        obj.custom_test = True
        obj.get_rezult()
        self.assertEqual(obj.success, True)
        self.assertRegex(
            obj.rezult,
            r'^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}'
        )

    # def test_get_rezult_custom_test_false(self):
    #     obj = OpenLead(self.json, True)
    #     obj.custom_test = False
    #     obj.get_rezult()
    #     print(obj.args_request)
    #     print(obj.rezult)
    #     self.assertEqual(obj.success, True)
    #     self.assertRegex(
    #         obj.rezult,
    #         r'^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}'
    #     )


class TestResponse:
    def __init__(self, status_code):
        self.status_code = status_code

    def get_response(self):
        response = requests.models.Response()
        response.status_code = self.status_code
        response._content = json.dumps({"id": 254}).encode('utf-8')
        return response

    def get_wrong_response(self):
        return self.get_response().text


def do():
    return {"d": "1"}


class CityBankesTestCase(TestCase):
    def setUp(self) -> None:
        def define_valid_json():
            return True

        self.define_valid_json = define_valid_json

    def test_init(self):

        self.CB = CityBankes()
        print(self.CB.cities_path)
        # print(self.CB.__dict__)

    def test_do_json(self):
        self.CB = CityBankes()
        self.CB.define_valid_json = self.define_valid_json
        self.CB.response_json = {'id': 'тут ничего нет'}
        self.CB.do_json()

    def test_test_do_json_AlfaCity(self):
        self.CB = AlfaCity()
        self.CB.define_valid_json = self.define_valid_json
        self.CB.response_json = {'values': 'тут ничего нет!!!'}
        self.CB.JC = JsonCustom(f'{os.environ.get("cityes_path")}test_do_json_AlfaCity.json')
        print(self.CB.do_json())

    def test_test(self):
        from custom_requests import ResponseGarant

        class YandexRequest(ResponseGarant):
            def __init__(self):
                super().__init__()
                self.method = 'get'
                self.url = 'https://ya.ru/'

            def do_status_code(self):
                self.success = True
                return self.response.text

        yr = YandexRequest()
        yr.get_rezult()

        if yr.success is True:
            print('Выполним условия в случае успеха')
        else:
            print('Выполним условия в случае неудачи')


class AlfaCityTestCase(TestCase):
    def setUp(self):
        self.ACTC = AlfaCity()

    def test_init(self):
        print(self.ACTC.__dict__)

    def test_define_valid_json(self):
        self.ACTC.response_json = {
            "values": []
        }
        print(self.ACTC.define_valid_json())

    def test_get_response(self):
        self.ACTC.get_response = TestResponse(200).get_response
        print(self.ACTC.get_response())

    def test_get_rezult(self):
        self.ACTC.get_response = TestResponse(200).get_response
        self.ACTC.get_rezult()


class VTBtokenTestCase(TestCase):
    def setUp(self):
        self.obj = VTBToken()
        print(self.obj.cert)

    def test_get_rezult(self):
        print(self.obj.path_vtb_token)
        print(self.obj.credits)

        print(self.obj.get_rezult())
        print(self.obj.get_response_functions()())

        print(self.obj.args_request)


class OpenTestCase(TestCase):
    def setUp(self):
        self.OTC = Open()
        self.OTC.test = test

    def test_init(self):
        print(self.OTC.__dict__)


class OpenCityTestCase(TestCase):
    def setUp(self):
        self.OCTC = OpenCity()
        # self.OCTC.test = test

    def test_init(self):
        print(self.OCTC.__dict__)

    def test_do_json(self):
        self.OCTC.response_json = {}
        print(self.OCTC.do_json())

    def test_get_rezult(self):
        print(self.OCTC.get_rezult())


# class OpenLeadScoringTestCase(TestCase):
#     def get_response_test(self):
#         return "Заглушка"
#
#     def get_response_production(self):
#         return "Рабочая"
#
#     def setUp(self) -> None:
#         json = {
#             "inns": [
#                 "1234567890",
#                 "0987654321",
#                 "7743013901"
#             ]
#         }
#         self.obj = OpenLeadScoring(json, True)
#
#         self.obj.get_response_test = self.get_response_test()
#         self.obj.get_response_production = self.get_response_production()
#
#     def test_custom_test_none(self):
#         self.obj = OpenLeadScoring({})
#         print(self.obj.__dict__)
#
#     def test_custom_test_true_custom_test_true(self):
#         self.obj.custom_test = True
#         self.assertEqual(self.obj.get_response_functions(), "Заглушка")
#
#     def test_custom_test_true_custom_test_false(self):
#         self.obj.custom_test = False
#         self.assertEqual(self.obj.get_response_functions(), "Рабочая")
#
#     def test_custom_test_false_custom_test_false(self):
#         self.obj.custom_test = False
#         self.obj.test = False
#         self.assertEqual(self.obj.get_response_functions(), "Рабочая")


class MoeDeloTestCase(TestCase):
    def setUp(self) -> None:
        self.json = {
            "Fio": "Jack",
            "Email": "test222.tester@moedelo.org",
            "Phone": "+7 (904) 266-15-42",
            "Inn": "9725074920",
            "Product": "Buro",
            "UtmSource": "[Имя партнёра]",
            "UtmCampaign": "[Имя компании]",
            "AccessType": "0"
        }

        self.obj = MoeDelo()


class PSBParentTestCase(TestCase):
    def setUp(self):
        self.PSBPTC = PSBParent()
        self.PSBPTC.test = test

    def test_init(self):
        print(self.PSBPTC.__dict__)


def get_session():
    return requests.session()


class PSBTestCase(TestCase):
    def setUp(self):
        with requests.session() as session:
            self.PSBTC = PSB(session)
            self.PSBTC.test = test

    def test_init(self):
        print(self.PSBTC.__dict__)

    def test_create_token(self):
        print(self.PSBTC.create_token())

    def test_get_response(self):
        print(self.PSBTC.get_response())

    def test_receive_condition(self):
        print(self.PSBTC.receive_condition())


class PSBCityTestCase(TestCase):
    def setUp(self):
        with requests.session() as session:
            self.PSBVTC = PSBCity(session)
            self.PSBVTC.test = test

    def test_init(self):
        print(self.PSBVTC.__dict__)

    def test_get_response(self):
        print(self.PSBVTC.get_response())

    def test_get_rezult(self):
        print(self.PSBVTC.get_rezult())

    def test_do_json(self):
        print(self.PSBVTC.do_json())


class PSBScoringTestCase(TestCase):
    def setUp(self):
        DefineTodaySession().write()
        self.session = LoadSession().get()
        self.json = {'inn': '27414792540'}
        self.obj = PSBScoring(self.json, self.session)

    def test_INIT(self):
        print(self.obj.__dict__)

    def test_get_response(self):
        if self.obj.access_token is not None:
            response = self.obj.get_response()
            print(response)
            print(self.obj.json)
            print(self.obj.access_token)

    def test_get_response_json(self):
        if self.obj.access_token is not None:
            self.obj.json = {'inn': 'tyrtyeryrt'}
            print(self.obj.url)
            print(self.obj.get_response().json())


class TokenTestCase(TestCase):
    def setUp(self) -> None:
        ERROR_AUT_KEY_VAL_CHOICES = (
        ('reason', 'Unauthorized'), ('errorMessage', 'the header <Authorization> was not received in the request'))
        self.obj = Aut(VTBToken, ERROR_AUT_KEY_VAL_CHOICES)

    def test_0(self):
        print(self.obj.__dict__)

    def test_1(self):
        print(self.obj.get())

    def test_2(self):
        print(self.obj.write())




class PSBLeadTestCase(TestCase):
    def setUp(self):
        DefineTodaySession().write()
        self.session = LoadSession().get()
        self.json = {
            "inn": '9725074920',
            "name": 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ВЕЛ-ТОРГ"',
            "need_s_schet": True,
            "need_r_schet": True,
            "fio": 'РОМАНОВ НИКОЛАЙ ВАСИЛЬЕВИЧ',
            "phone": '79771036772',
            "email": "yj@mail.ru",
            "city_id": '1',
            "comment": ''
        }
        self.obj = PSBLead(self.json, self.session)

    def test_get_response(self):
        print(self.obj.get_response())

    def test_get_rezult(self):
        print(self.obj.get_rezult())


class RaifazenTestCase(TestCase):
    def setUp(self):

        self.json = {
              "meta": {
                "partnerID": "000052",
                "businessProduct": "Corporate Account Opening XS",
                # "refID": "de1c69b5-51de-000c-9ed7-14b0000dd5df"
              },
              "data": {
                "city": "DD8FDE573A964072F998590C212121E0",
                "companyName": 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "МОМЕНТ"',
                "inn": '5614087362',
                "comment": '',
                "personName": {
                  "firstName": 'САВЕЛЬЕВ',
                  "lastName": 'АНАТОЛИЙ',
                  "middleName": 'КОНСТАНТИНОВИЧ'
                },
                "communicationChannels": {
                  "phone": {
                    "countryCode": '+7',
                    "phoneNumber": '9068390072'
                  }
                },

              }
            }
        self.obj = Raifazen(self.json)

    def test_0(self):
        print(self.obj.get_rezult())
        print(self.obj.response.text)

    def test_init(self):
        print(self.obj.__dict__)


class PSBTokenTestCase(TestCase):
    def test_0(self):
        obj = PSBToken(True)

        print(obj.get_rezult())


    def test_1(self):
        # {'code': 404, 'status': 'NOT_EXISTS', 'message': 'Создание заявки с данным ИНН разрешено'}
        test = False


        inns = ["6382094062", "5007117617", "9705184265", "4705097662", "7734465242", "7813668661", "6320072051", "9719031558", "9723172375", "9704171432", "9725098952", "9725098960", "9725099000", "9725099032", "9703113607", "9727011971", "9726024618", "9704171601", "9728076523", "9727011925", "9727011932", "9728076587", "9701224453", "9701224478", "9728076594", "9727011989", "9729331977", "9725098977", "9705180415", "9726024590", "9727011940", "9727011957", "9728076604", "9729331952", "9727012012", "9725098945", "9726024583", "9728076611", "9718205890", "9703113597", "9727011918", "9706027434", "5009133639", "5262389062", "5032348840", "5029273458", "5075041684", "5018213256", "1684009258", "700006760", "5032348858", "5045069026", "3513003845", "1832165912", "1831207863", "5906175062", "1655489708", "1683010476", "1684009265", "1650418887", "5257212077", "1685008190", "3527024852", "5031148849", "9724109591", "5031148831", "5017130695", "5027311838", "1674003480", "1675001816", "6168118814", "1685008144", "5017130688", "5263150855", "5906175055", "1674003465", "1655489715", "5031148856", "1686020850", "1686020835", "1655489698", "5260487674", "3700000844", "5003154230", "5040182162", "3521007120", "3522004919", "5005072569", "1655489578", "1685008151", "5018213249", "5012108960", "3100009700", "9102286098", "1832165920", "5044137481", "1644101338", "1655489641", "1673003293", "9408000035"]
        for inn in inns[0:1]:
            json = {'inn': inn}

            obj_s = PSBScoring(json, test)


            print(obj_s.get_rezult())
            print(obj_s.args_request)
            # print(obj_s.response_status_code)
            # print(obj_s.response.text)
            # print(obj_s.response.headers)
            time.sleep(1)

    def test_1_1(self):
        def write_token():
            return None

        test = True
        json = {'inn': "6382094062"}
        obj_s = PSBScoring(json, test)
        obj_s.response_json = {'name': 'Unauthorized', 'message': 'Your request was made with invalid credentials.', 'code': 0, 'status': 401}
        obj_s.write_token = write_token
        print(obj_s.do_json())


    def test_2(self):
        json = {
            "inn": '9408000035',
            "name": 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ВЕЛ-ТОРГ"',
            "need_s_schet": True,
            "need_r_schet": True,
            "fio": 'РОМАНОВ НИКОЛАЙ ВАСИЛЬЕВИЧ',
            "phone": '79895085349',
            "email": "yj@mail.ru",
            "city_id": '1',
            "comment": ''
        }

        test = True


        obj_s = PSBLead(json, test)
        print(obj_s.get_rezult())
        # print(obj_s.response_json)

    def test_3(self):

        def f(*args):
            print(args)

        args = ()
        f(*args)


class RosBankLeadTestCase(TestCase):
    def test_test(self):
        json = {
            'inn': '7751252660',
            'contact_comment': 'тест',
            'contact_name': 'ТЕСТОВА ТЕСТА ТЕСТОВНА',
            'phone': '+79167819499',
            'is_registered_inn': True,
            'is_accept_info': True,
            'mgm_code': 'K10X5D1',
            # 'webmaster_id': '',
            'region_code': '77',
            'google_id': '777.777',
        }
        obj = RosBankLead(json)
        obj.get_rezult()
        print(obj.response.request.headers)
        print(obj.response.text)
        print(obj.response.content)
        print(obj.response.json())
#         {"success":true,"id":2192696}


class KonturTestCase(TestCase):
    def test_0(self):
        # json = {
        #     "ProspectiveSaleId": "8d1a3f97-fabd-46b9-972c-eb3c2437a913",
        #     "Organization": {
        #         "Inn": "7654776644",
        #         "IsPhysical": False,
        #         "Name": "ООО «Боевые Робоединороги»",
        #         "Region": "66",
        #         "City": "Екатеринбург",
        #         "Address": "ул. Малопрудная, д. 5"
        #     },
        #     "CountryCode": "RU",
        #
        #     "InternalProductId": "Evrika",
        #     "PartnerCode": "0800",
        #     "ManagerCode": "08001",
        #     "Supplier": {
        #         "PartnerCode": "1000",
        #         "Inn": "0300797309",
        #         "Kpp": "030001001"
        #     },
        #     "Type": 1,
        #     "LifeTime": "2023-08-12T10:14:06",
        #
        #     "Brief": {
        #         "Type": "05a05a89-2c0c-4087-a3bf-f45df4af3e79"
        #     },
        #     "SpecialScheme": 0,
        # }
        json = {
            # "ProspectiveSaleId": "6c2ee486-eb32-4515-a3aa-0bc40825b39a",
            "Organization": {
                "Inn": "7654776644",
                # "Kpp": "765401001",
                "IsPhysical": False,
                "Name": "ООО «Боевые Робоединороги»",
                "Region": "66",
                "City": "Екатеринбург",
                "Address": "ул. Малопрудная, д. 5"
            },
            "CountryCode": "RU",
            "ForeignOrganization": None,
            "ExternalProductId": None,
            "InternalProductId": "Evrika",
            "PartnerCode": "b0000",
            # "ManagerCode": "08001",
            # "Supplier": {
            #     "PartnerCode": "1000",
            #     "Inn": "0300797309",
            #     "Kpp": "030001001"
            # },
            "Type": 1,
        }
        print(KonturCanCreate(json, True).get_rezult())

    def test_2(self):
        json = {
            # "ProspectiveSaleId": "7cd28409-4c7c-4b55-af5e-f388a3326124",
            "Organization": {
                "Inn": "7654776644",
                # "Kpp": "765401001",
                "IsPhysical": False,
                "Name": "ООО «Боевые Робоединороги»",
                # "Region": "66",
                "City": "Екатеринбург",
                "Address": "ул. Малопрудная, д. 5"
            },
            "Contacts": [
                {
                    "Name": "Кропоткин Василий Павлович",
                    "Position": "Директор",
                    "Phones": [
                        {
                            "Id": "98da9a79-55f2-46a0-bfa8-a50b8cbce3c4",
                            "Number": "+75554440011",
                            "AdditionalNumber": "123"
                        }
                    ],
                    # "Emails": [
                    #     {
                    #         "Address": "ooo@yandex.ru"
                    #     }
                    # ]
                }
            ],
            "Source": "www.source.ru",
            "CountryCode": "RU",
            "ForeignOrganization": None,
            "ExternalProductId": None,
            "InternalProductId": "Evrika",
            "PartnerCode": "b0000",
            # "ManagerCode": "08001",
            # "Supplier": {
            #     "PartnerCode": "1000",
            #     "Inn": "0300797309",
            #     "Kpp": "030001001"
            # },
            "Type": 1,
        }

        # json = {
        #     'ProspectiveSaleId': 'adf1e209-1308-4713-87a1-18f8c01995ef',
        #     "Contacts": [
        #         {
        #             "Name": "Кропоткин Василий Павлович",
        #             "Position": "Директор",
        #             "Phones": [
        #                 {
        #                     "Id": "98da9a79-55f2-46a0-bfa8-a50b8cbce3c4",
        #                     "Number": "+75554440011",
        #                     "AdditionalNumber": "123"
        #                 }
        #             ],
        #             "Emails": [
        #                 {
        #                     "Address": "ooo@yandex.ru"
        #                 }
        #             ]
        #         }
        #     ],
        #     "InternalProductId": "Evrika",

        # }
        print(KonturProspectiveSales(json, True).get_rezult())

class DevelopTest(TestCase):
    def test_0(self):
        inn = '800009370'
        print(mutation_inn(inn))


class PSBdtfmqueueTestCase(TestCase):
    def test_0(self):
        json_dict = {
            "inns": ['665813932028']
        }
        obj = PSBdfmqueue(json_dict, False).get_obj_rezult()
        print(obj.response.text)
        print()