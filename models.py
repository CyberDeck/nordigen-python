"""Nordigen API aendpoints."""
import json
import requests
import settings


class Endpoints():
    """Nordigen API aendpoints."""

    def __init__(self):
        """Variables used trough all api calls."""
        self.ng_token = None
        self.agreements = []
        self.enduser_id = None
        self.reference_id = None
        self.aspsp_id = None
        self.country = None
        self.requisitions_id = None

    def _get_response(self, method: str, url: str, data: dict) -> json:
        """
        Handle actual request to NG API.

        Args:
            method (str): Request method: GET | POST
            url (str): Request URL
            data (dict): GET payload or POST data

        Raises:
            HTTPError: On status code other than 200

        Returns:
            json: Responce json
        """
        base_headers = {
            'accept': 'application/json',
            'Authorization': f'Token {self.ng_token}',
            'Content-Type': 'application/json'
        }

        if method == 'GET':
            response = requests.get(url, verify=True, headers=base_headers, params=data)
        elif method == 'POST':
            response = requests.post(url, verify=True, headers=base_headers, data=json.dumps(data))

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            raise

        return response.json()

    def aspsps(self, country: str) -> list:
        """
        Get all avialable ASPSPs (banks) in a given country.

        Args:
            country (str): Two-character country code

        Returns:
            list: Aspsps in given country
        """
        self.country = country
        payload = {'country': self.country}
        aspsps = self._get_response('GET', f'{settings.BASE_URL}aspsps/', payload)
        return aspsps

    def enduser_agreement(self, aspsp_id: str, max_historical_days: int = 90):
        """
        Create end user agreement.

        Args:
            aspsp_id (str): Unique identifier of the end users bank
            max_historical_days (int, optional): Length of the transaction history.
                                                 Defaults to 90.
        """
        self.aspsp_id = aspsp_id
        data = {
            'enduser_id': self.enduser_id,
            'max_historical_days': max_historical_days,
            'aspsp_id': self.aspsp_id
        }

        response_data = self._get_response('POST', f'{settings.BASE_URL}agreements/enduser/', data)
        self.agreements.append(response_data['id'])

    def requisitions(self):
        """Create requisition for creating links and retrieving accounts."""
        data = {
            'redirect': settings.REDIRECT_URL,
            'reference': self.reference_id,
            'enduser_id': self.enduser_id,
            'agreements': self.agreements
        }
        response_data = self._get_response('POST', f'{settings.BASE_URL}requisitions/', data)
        self.requisitions_id = response_data['id']

    def requisition_link(self) -> str:
        """
        Create a redirect link for the end user to ASPSP.

        Returns:
            str: Redirect link
        """
        data = {
            'aspsp_id': self.aspsp_id
        }
        response_data = self._get_response(
            'POST', f'{settings.BASE_URL}requisitions/{self.requisitions_id}/links/', data
        )
        return response_data['initiate']

    def accounts(self) -> list:
        """
        List accounts.

        Returns:
            list: Accounts
        """
        response_data = self._get_response(
            'GET', f'{settings.BASE_URL}requisitions/{self.requisitions_id}/', {}
        )

        return response_data['accounts']

    def acc_data(self, accounts: list) -> dict:
        """
        Get account data - details, balances & transactions. Save data into json.

        Args:
            accounts (list): Account IDs

        Returns:
            dict: All accounts data
        """
        ret_dict = {}

        # Get details/balances/transactions for all accounts
        for acc in accounts:
            ret_dict[acc] = {}

            for url_path in ['details', 'balances', 'transactions']:
                response_data = self._get_response(
                    'GET', f'{settings.BASE_URL}accounts/{acc}/{url_path}/', {}
                )

                # Save results
                with open(f'downloads/{acc}_{url_path}.json', 'w') as save_file:
                    json.dump(response_data, save_file)

                ret_dict[acc][url_path] = response_data

        return ret_dict
