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

    # def test_get_rezult_false(self):
    #     obj = AlfaScoring(self.json, False)
    #     obj.get_rezult()
    #     self.assertEqual(obj.success, True)
    #     self.assertIn(obj.rezult, ['????????????????', '??????????'])

    def test_get_rezult_true(self):
        obj = AlfaScoring(self.json, True)
        obj.get_rezult()
        self.assertEqual(obj.success, True)
        self.assertIn(obj.rezult, ['????????????????', '??????????'])


class AlfaLeadTestCase(TestCase):
    def setUp(self):
        self.key = os.environ.get('alfabank_dict_key')
        self.json = {
            'organizationInfo': {
                'organizationName': '???????????????? ?? ???????????????????????? ???????????????????????????????? "??????-????????"',
                'inn': '9725074920',
            },
            'contactInfo': [{
                "fullName": '?????????????? ?????????????? ????????????????????',
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
        self.assertRegex(obj.do_json(), r'^???????????? ?????????? ??????????????$')

    def test_do_json_LEADS_LIMIT_ERROR(self):
        obj = AlfaLead(self.json, True)
        obj.response_json = {'errors': [
            {'status': 403, 'code': 'LEADS_LIMIT_ERROR', 'title': 'Leads limit exceeded',
             'detail': 'The allowed limit of 45 leads has already exceeded.'}]}
        self.assertRegex(obj.do_json(), r'^???????????????? ??????????$')

    def test_do_json_validationError(self):
        obj = AlfaLead(self.json, True)
        obj.response_json = {'errors': [{'status': 400, 'code': 'validationError',
                                         'detail': '???????????????? 79099096723986 ???????? $.contactInfo[*].phoneNumber ???? ?????????????????????????? ?????????????????????? ?????????????????? 7\\d{10}',
                                         'title': '???????????? ?????????????????? ????????????', 'meta': {
                'jexceptionMsg': 'javax.validation.ValidationException: ???????????????? 79099096723986 ???????? $.contactInfo[*].phoneNumber ???? ?????????????????????????? ?????????????????????? ?????????????????? 7\\d{10}'}}]}
        self.assertRegex(obj.do_json(), r'???? ?????????????????????????? ?????????????????????? ??????????????????')


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
            "leads": [
                {
                    "inn": '4400008354',
                    "productCode": "Payments",
                },
                {
                    "inn": '6679151716',
                    "productCode": "Payments",
                }
            ]
        }

    def test_test(self):
        obj = VTBScoring(self.json)  #
        obj.get_rezult()
        content = b'{"leads":[{"inn":"6679151716","productCode":"Payments","responseCode":"POSITIVE","responseCodeDescription":"\xd0\x9b\xd0\xb8\xd0\xb4 \xd0\xbc\xd0\xbe\xd0\xb6\xd0\xb5\xd1\x82 \xd0\xb1\xd1\x8b\xd1\x82\xd1\x8c \xd0\xb2\xd0\xb7\xd1\x8f\xd1\x82 \xd0\xb2 \xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd1\x83"},{"inn":"4400008354","productCode":"Payments","responseCode":"POSITIVE","responseCodeDescription":"\xd0\x9b\xd0\xb8\xd0\xb4 \xd0\xbc\xd0\xbe\xd0\xb6\xd0\xb5\xd1\x82 \xd0\xb1\xd1\x8b\xd1\x82\xd1\x8c \xd0\xb2\xd0\xb7\xd1\x8f\xd1\x82 \xd0\xb2 \xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd1\x83"}]}'
        cont = content.decode()
        print(cont)
        print(json.loads(cont))
        # j = "{'leads': [{'inn': '4400008354', 'productCode': 'Payments', 'responseCode': 'POSITIVE', 'responseCodeDescription': '?????? ?????????? ???????? ???????? ?? ????????????'}, {'inn': '6679151716', 'productCode': 'Payments', 'responseCode': 'POSITIVE', 'responseCodeDescription': '?????? ?????????? ???????? ???????? ?? ????????????'}]}"
        # print()
        # print(json.loads(j))
        # test_res = json.loads()
        # print(test_res)
        # print(type(test_res))

    def test_get_rezult(self):
        obj = VTBScoring(self.json)
        obj.get_rezult()
        self.assertEqual(obj.success, True)
        self.assertEqual(sorted([dict_client['inn'] for dict_client in obj.rezult]),
                         sorted([json['inn'] for json in self.json['leads']]))

    def test_do_json_unauthorized(self):
        obj = VTBScoring(self.json)
        obj.response_json = {'httpCode': '401', 'httpMessage': 'Unauthorized',
                             'moreInformation': "<BackErr> needConfirm"}
        obj.do_json()
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
                    "phone": "+7123456789",
                    "consentOnPersonalDataProcessing": True,
                    "inn": "547779835982",
                    "city": "????????????",
                    "productCode": "Payments",
                    "sourceLeadId": "02",
                },
                {
                    "phone": "+7123456789",
                    "consentOnPersonalDataProcessing": True,
                    "inn": "547779835982",
                    "city": "????????????",
                    "productCode": "Payments",
                    "sourceLeadId": "01",
                }
            ]
        }

    def test_get_rezult(self):
        obj = VTBLead(self.json)
        obj.custom_test = True
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


class TochkaLeadTestCase(TestCase):
    def setUp(self):
        self.json = {
            "token": '',
            "request": {
                'inn': '9725074920',
                'name': "?????? '??????-????????'",
                'last_name': '??????????????',
                'first_name': '??????????????',
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
        self.assertRegex(str(obj.rezult), r'^[0-9]{5}$|^?????????????? ???????????????? ??????.$|^????????????: ???????????? ?? ??????')


class TochkaRegistryUrTestCase(TestCase):
    def setUp(self) -> None:
        self.json = {
            "token": '',
            "request": {
                'snils': '083-367-324-77',
                'org_form': 'ltd',
                'inn': '9725074920',
                'last_name': '??????????????',
                'first_name': '??????????????',
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
            "person_firstname": "??????",
            "person_surname": "??????????????",
            "person_middlename": "????????????????",
            "person_phone": "79000000000",
            "comment": "",
            "stg": [
                "ACCOPEN"
            ],
            "company_name": "???? ?????????????? ?????? ????????????????"
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
            "person_firstname": "??????????",
            "person_surname": "??????????????????",
            "person_middlename": "??????????????????????????",
            "person_phone": "79384965043",
            "comment": "",
            "stg": [
                "ACCOPEN"
            ],
            "company_name": "???? ?????????????????? ?????????? ??????????????????????????"
        }
        obj = ModuleLead(json, True)
        obj.response_json = {'status': 'ok', 'response': {'page': 1, 'pageSize': 15, 'total': 78, 'list': [

            {'id': 'CF2D5672-16DF-408A-9BD9-CE2613D8E05A', 'num': 671359, 'dadd': '2021-10-13T19:30:10.903',
             'state': 'success', 'lastUpd': '2021-10-15T18:05:00.373', 'stg': ['ACCOPEN'], 'inn': '7713485142',
             'client_name': '?????? "????????????"', 'person_phone': '79153632139', '__num_searchable': '671359'},
            {'id': '848B89C1-498D-4944-9B89-F19C7408D32A', 'num': 664406, 'dadd': '2021-10-11T16:21:59.15',
             'state': 'success', 'lastUpd': '2021-10-13T19:04:53.587', 'stg': ['ACCOPEN'], 'inn': '9723126097',
             'client_name': '?????? "??????????"', 'person_phone': '79851462972', '__num_searchable': '664406'},
            {'id': '05881C15-7EE9-4EF1-A5A5-39010DE49D46', 'num': 662579, 'dadd': '2021-10-11T00:09:49.093',
             'state': 'decline.double', 'lastUpd': '2021-10-11T00:10:00.277', 'stg': ['ACCOPEN'], 'inn': '9704091265',
             'client_name': '?????? "????????????"', 'person_phone': '79151352742', '__num_searchable': '662579'},
            {'id': 'F4E3F811-0160-4487-AFD5-B0285241A52B', 'num': 662578, 'dadd': '2021-10-11T00:06:37.47',
             'state': 'waitformeeting', 'lastUpd': '2022-04-26T20:53:04.157', 'stg': ['ACCOPEN'], 'inn': '7726484266',
             'client_name': '?????? "??????"', 'person_phone': '79151352686', '__num_searchable': '662578'},
            {'id': '9D0A9185-2F8B-4BBE-87E3-5729C1013D88', 'num': 662576, 'dadd': '2021-10-11T00:01:19.867',
             'state': 'decline.double', 'lastUpd': '2021-10-11T00:05:00.433', 'stg': ['ACCOPEN'], 'inn': '262517148226',
             'client_name': '???? ?????????????? ?????????????? ????????????????????????', 'person_phone': '79153635015',
             '__num_searchable': '662576'},
            {'id': '75216E9F-6200-4FF6-92FE-54B3CE189A7E', 'num': 650883, 'dadd': '2021-10-06T14:43:03.7',
             'state': 'success', 'lastUpd': '2021-10-08T20:03:48.6', 'stg': ['ACCOPEN'], 'inn': '330646707810',
             'client_name': '???????????????????????????? ?????????????????????????????? ?????????????? ?????????? ?????????????? ????????', 'person_phone': '79151360842',
             '__num_searchable': '650883'},
            {'id': '8FF57C80-19D2-4E9F-AEB1-053F0F948E56', 'num': 646306, 'dadd': '2021-10-04T23:19:13.58',
             'state': 'decline.double', 'lastUpd': '2021-10-04T23:20:00.497', 'stg': ['ACCOPEN'], 'inn': '9704090896',
             'client_name': '?????? "??????????"', 'person_phone': '79851463060', '__num_searchable': '646306'},
            {'id': 'D2CDE4C9-271B-41F1-979B-35A5782B6B64', 'num': 1738110, 'dadd': '2022-05-25T13:10:03.013',
             'state': 'init', 'lastUpd': '2022-05-25T13:10:03.013', 'stg': ['ACCOPEN'], 'inn': '383702760141',
             'client_name': '???? ?????????????????? ?????????? ??????????????????????????', 'person_phone': '79384965043',
             '__num_searchable': '1738110'},
            {'id': 'BA3A89BD-EECE-4AE5-A3A7-067EFB41DC36', 'num': 646288, 'dadd': '2021-10-04T23:13:12.113',
             'state': 'decline.double', 'lastUpd': '2021-10-04T23:15:00.48', 'stg': ['ACCOPEN'], 'inn': '9703050523',
             'client_name': '?????? "????????????"', 'person_phone': '79851462894', '__num_searchable': '646288'},
            {'id': '7B563227-3115-4ACC-9BA4-2A14A73DE40D', 'num': 646285, 'dadd': '2021-10-04T23:11:49.903',
             'state': 'decline.double', 'lastUpd': '2021-10-04T23:15:00.48', 'stg': ['ACCOPEN'], 'inn': '771573339751',
             'client_name': '???? ???????????????? ???????????? ????????????????????', 'person_phone': '79851460848',
             '__num_searchable': '646285'},
            {'id': 'E344DC95-9A95-4862-B6CA-74B785747E8E', 'num': 643485, 'dadd': '2021-10-03T13:15:26.03',
             'state': 'success', 'lastUpd': '2021-10-07T13:04:17.42', 'stg': ['ACCOPEN'], 'inn': '9704090617',
             'client_name': '?????? "??????"', 'person_phone': '79850875811', '__num_searchable': '643485'},
            {'id': 'DA004D55-A43A-4051-9490-C402607BC7BF', 'num': 643484, 'dadd': '2021-10-03T13:13:17.51',
             'state': 'success', 'lastUpd': '2021-10-07T13:04:17.42', 'stg': ['ACCOPEN'], 'inn': '052999963528',
             'client_name': '???????????????????????????? ?????????????????????????????? ?????????????????????? ???????????? ??????????????????????',
             'person_phone': '79153632139', '__num_searchable': '643484'},
            {'id': '42A654DF-3D76-4686-B8BE-0D1C0AEC5F6A', 'num': 643483, 'dadd': '2021-10-03T13:05:36.607',
             'state': 'success', 'lastUpd': '2021-10-06T20:33:48.473', 'stg': ['ACCOPEN'], 'inn': '9723124646',
             'client_name': '?????? "??????"', 'person_phone': '79851465477', '__num_searchable': '643483'},
            {'id': '8410040F-7E2D-4B36-81A8-E9A76B40E85E', 'num': 643481, 'dadd': '2021-10-03T13:03:41.653',
             'state': 'decline.double', 'lastUpd': '2021-10-03T13:05:00.923', 'stg': ['ACCOPEN'], 'inn': '9703049408',
             'client_name': '?????? "????????????????"', 'person_phone': '79166529856', '__num_searchable': '643481'},
            {'id': '5E9ADBEE-69D5-4398-B3DA-8191EE96A8D8', 'num': 643479, 'dadd': '2021-10-03T13:01:11.41',
             'state': 'success', 'lastUpd': '2021-10-06T20:33:48.473', 'stg': ['ACCOPEN'], 'inn': '343520598450',
             'client_name': '???????????????????????????? ?????????????????????????????? ???????????? ?????????????? ???????????? ????????', 'person_phone': '79153631180',
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
            "Fio": "Jack",
            "Email": "tet222.teste@moedelo.org",
            "Phone": "+7 (909) 266-15-42",
            "Inn": "9725074920",
            "Product": "Buro",
            "UtmSource": "partner.1326.BIZ",
            "Comment": "???????????????? ????????????"
        }

        self.obj = MoeDeloLead(self.json)

    def test_get_rezult_custom_test_true(self):
        obj = MoeDeloLead(self.json, True)
        obj.custom_test = True
        obj.get_rezult()

        self.assertEqual(obj.success, True)
        self.assertRegex(obj.rezult, r'^[0-9]{3}-[0-9]{3}-[0-9]{3}$')

    # def test_get_rezult_custom_test_false(self):
    #     obj = MoeDeloLead(self.json, False)
    #     obj.custom_test = False
    #     print(obj.get_rezult())
    #     self.assertEqual(obj.success, True)
    #     self.assertRegex(obj.rezult, r'^[0-9]{2}[0-9]{3}[0-9]{3}$')

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
    #     obj.get_rezult()
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


class OpenLeadTestCase(TestCase):
    def setUp(self) -> None:
        self.json = {
            'full_name': '???????????? ???????? ????????????????',
            'inn': '688153834076',
            'phone': '+79771036772',
            'email': 'abc5462t@mail.ru',
            'city': "????????????",
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
        print(self.CB.__dict__)

    def test_do_json(self):
        self.CB = CityBankes()
        self.CB.define_valid_json = self.define_valid_json
        self.CB.response_json = {'id': '?????? ???????????? ??????'}
        self.CB.do_json()

    def test_test_do_json_AlfaCity(self):
        self.CB = AlfaCity()
        self.CB.define_valid_json = self.define_valid_json
        self.CB.response_json = {'values': '?????? ???????????? ??????!!!'}
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
            print('???????????????? ?????????????? ?? ???????????? ????????????')
        else:
            print('???????????????? ?????????????? ?? ???????????? ??????????????')


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

    def test_get_rezult(self):
        print(self.obj.get_rezult())


class OpenTestCase(TestCase):
    def setUp(self):
        self.OTC = Open()
        self.OTC.test = test

    def test_init(self):
        print(self.OTC.__dict__)


class OpenCityTestCase(TestCase):
    def setUp(self):
        self.OCTC = OpenCity()
        self.OCTC.test = test

    def test_init(self):
        print(self.OCTC.__dict__)

    def test_do_json(self):
        print(self.OCTC.do_json())

    def test_get_rezult(self):
        print(self.OCTC.get_rezult())


# class OpenLeadScoringTestCase(TestCase):
#     def get_response_test(self):
#         return "????????????????"
#
#     def get_response_production(self):
#         return "??????????????"
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
#         self.assertEqual(self.obj.get_response_functions(), "????????????????")
#
#     def test_custom_test_true_custom_test_false(self):
#         self.obj.custom_test = False
#         self.assertEqual(self.obj.get_response_functions(), "??????????????")
#
#     def test_custom_test_false_custom_test_false(self):
#         self.obj.custom_test = False
#         self.obj.test = False
#         self.assertEqual(self.obj.get_response_functions(), "??????????????")


class MoeDeloTestCase(TestCase):
    def setUp(self) -> None:
        self.json = {
            "Fio": "Jack",
            "Email": "test222.tester@moedelo.org",
            "Phone": "+7 (904) 266-15-42",
            "Inn": "9725074920",
            "Product": "Buro",
            "UtmSource": "[?????? ????????????????]",
            "UtmCampaign": "[?????? ????????????????]",
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


class PSBLeadTestCase(TestCase):
    def setUp(self):
        DefineTodaySession().write()
        self.session = LoadSession().get()
        self.json = {
            "inn": '9725074920',
            "name": '???????????????? ?? ???????????????????????? ???????????????????????????????? "??????-????????"',
            "need_s_schet": True,
            "need_r_schet": True,
            "fio": '?????????????? ?????????????? ????????????????????',
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
