import json
import uuid
from decouple import config

import requests


class WiseService:
    def __init__(self):
        self.main_url = 'https://api.sandbox.transferwise.tech'
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}",
        }
        profile_id = self._get_profile_id()
        self.profile_id = profile_id

    def _get_profile_id(self):
        url = self.main_url + '/v1/profiles'
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            resp = resp.json()
            return [a['id'] for a in resp if a['type'] == 'personal'][0]
        else:
            print(resp)
            raise ValueError("Bad request")

    def create_quote(self, amount):
        url = self.main_url + "/v2/quotes"
        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "BGN",
            "targetAmount": amount,
            "profile": self.profile_id,
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))

        if resp.status_code == 200:
            # print(resp.json())
            resp = resp.json()
            return resp["id"]
        else:
            print(resp)
            raise ValueError("Bad requests in stage v2")

    def create_recipient_account(self, full_name, iban):
        url = self.main_url + "/v1/accounts"
        data = {
            "currency": "BGN",
            "type": "iban",
            "profile": self.profile_id,
            "accountHolderName": full_name,
            "legalType": "PRIVATE",
            "details": {"iban": iban},
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))

        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        else:
            print(resp)
            raise ValueError("Error in stage 2 recepient")

    def create_transfer(self, target_account_id, quote_id):
        customer_transaction_id = str(uuid.uuid4())
        url = self.main_url + "/v1/transfers"
        data = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,
            "details": {},
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))

        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        else:
            print(resp)
            raise ValueError("Error in stage 3")

    def fund_transfer(self, transfer_id):
        url = self.main_url + \
            f"/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        resp = requests.post(url, headers=self.headers)

        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        else:
            print(resp)
            raise ValueError("Error in stage 4 Fund")