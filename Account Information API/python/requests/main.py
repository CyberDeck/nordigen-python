"""Quickstart Guide."""
from datetime import datetime as dt
import json
import requests

# Base api URL
BASE_URL = 'https://ob.nordigen.com/api/'

# Access token from https://ob.nordigen.com/tokens/
NG_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


def execute_request(method: str, url: str, data: dict) -> json:
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
        'Authorization': f'Token {NG_TOKEN}',
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


def main():
    """Account Information api logic."""
    # 1 Get aspsps (banks) based on country
    # https://nordigen.com/en/account_information_documenation/integration/bank-selection-ui/#find_banks
    #
    # Here you can get all supported bank ids

    # GET arguments
    payload = {'country': 'FI'}

    # Get all aspsps - this can be skipped
    aspsps = execute_request('GET', f'{BASE_URL}aspsps/', payload)

    # Get aspsp ID
    aspsp_id = aspsps[0]['id']

    # For now lets just use Revolut
    aspsp_id = 'REVOLUT_REVOGB21'

    # 2 Create end user agreement
    # https://nordigen.com/en/account_information_documenation/integration/quickstart_guide/#create_end_user_agreement
    #

    # Unique UUID (generated by you)
    enduser_id = 666

    # POST data
    # enduser_id: Unique UUID (generated by you)
    # max_historical_days: Length of the transaction history to be retrieved
    # aspsp_id: End users bank id - from previous step
    data = {
        'enduser_id': enduser_id,
        'max_historical_days': '90',
        'aspsp_id': aspsp_id
    }

    # Agreement ids
    agreements = []
    response_data = execute_request('POST', f'{BASE_URL}agreements/enduser/', data)
    agreements.append(response_data['id'])

    # s3 Build a Link
    # https://nordigen.com/en/account_information_documenation/integration/quickstart_guide/#build_a_link
    # To create a requisition
    #
    # redirect: URL that you will be redirected after aspsp login
    # reference: This has to be unique every time you call requisitions to Nordigen
    # enduser_id: from previous step
    # agreements: from previous response

    reference_id = dt.now().strftime("%Y%m%d%H%M%S")
    made_up_url = 'http://localhost/requisition'

    # POST data
    data = {
        'redirect': made_up_url,
        'reference': reference_id,
        'enduser_id': enduser_id,
        'agreements': agreements
    }
    response_data = execute_request('POST', f'{BASE_URL}requisitions/', data)
    requisitions_id = response_data['id']

    # 3.1 Redirect link for the end user to ASPSP
    #
    # POST data
    data = {
        'aspsp_id': aspsp_id
    }
    response_data = execute_request('POST', f'{BASE_URL}requisitions/{requisitions_id}/links/', data)

    print(f"1. Visit: {response_data['initiate']}")
    print("2. Authorise")
    # Wait until loginto aspsp
    input("And press Enter to continue...")

    # Redirect to aspsp login
    # After login this will redirect to made_up_url?ref=reference_id
    #  - redirects to http://localhost/requisition?ref=20210311125416

    # 4 List all accounts
    #
    response_data = execute_request('GET', f'{BASE_URL}requisitions/{requisitions_id}/', {})
    all_accounts = response_data['accounts']

    # 5 Get balances & transactions
    #
    for url_path in ['balances', 'transactions']:

        # Get balances/transactions for all accs
        for acc in all_accounts:
            print(f"Get {url_path} for account: {acc}")
            response_data = execute_request('GET', f'{BASE_URL}accounts/{acc}/{url_path}/', {})

            # Save as JSON
            with open(f'{acc}_{url_path}.json', 'w') as save_file:
                json.dump(response_data, save_file)


if __name__ == '__main__':
    main()