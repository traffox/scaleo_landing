from loguru import logger
import requests
import json
import os


logger.add('app.log', format='{time} {level} {message}', level='DEBUG', rotation='1 week', compression='zip')
API_KEY = os.getenv('API_KEY')


class API:
    reg_url = ("https://edem.scaletrk.com/api/v2/network/affiliates?api-key={}".format(API_KEY))
    login_url = ("https://edem.scaletrk.com/api/v2/network/get-login-link?api-key={}".format(API_KEY))
    reset_url = ("https://edem.scaletrk.com/api/v2/network/user/reset-password?api-key={}".format(API_KEY))

    reset_data = {
        'email': None
    }

    login_data = {
        'email': None,
        'password': None,
    }
    contact_telegram = {"type": 5, "account": None, "title": "Telegram"}

    reg_data = {
        'email': None,
        'firstname': 'Account',
        'lastname': 'A',
        'password': None,
        'password_repeat': None,
        'account_type': '1',
        'company_name': 'company',
        'contacts': '',
        'website_url': 'https://www.scaleo.io',
        'phone': '+(380)0000-000-000',
        'notes': 'info',
        'status': '1',
        'country': '1',
        'region': '1',
        'city': '1',
        'address': '1',
        'postal_code': '1',
        'tags': '1',
        'traffic_types': '1',
        'managers': '1',
        'image_data': '',
    }

    def __init__(self, email, password=None, repassword=None, telegram=None):

        self.status_code = None
        self.content = None

        if not password:
            """recover account"""
            self.data = self.reset_data
            self.data['email'] = email
            self.url = self.reset_url
            logger.info(f"Recover password - {email} - {telegram}")
        elif not repassword:
            """login"""
            self.data = self.login_data
            self.data['email'] = email
            self.data['password'] = password
            self.url = self.login_url
            logger.info(f"Login - {email} - {telegram}")
        else:
            """registration"""
            self.data = self.reg_data
            self.data['email'] = email
            self.data['password'] = password
            self.data['repassword'] = repassword
            if telegram:
                contacts = []
                self.contact_telegram['account'] = telegram
                contacts.append(self.contact_telegram)
                r = json.dumps(contacts)
                self.data['contacts'] = r
            self.url = self.reg_url
            logger.info(f"Registration - {email} - {telegram}")

    def send_data(self):
        try:
            # d = json.dumps(self.data)
            response = requests.post(self.url, data=self.data)
            logger.info(f'{response.status_code}  -  {response.content}')
            self.content = json.loads(response.content)
            self.status_code = response.status_code
        except Exception as e:
            logger.error(e)
