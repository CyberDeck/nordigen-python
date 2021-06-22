"""Flask app."""
from datetime import datetime as dt
import os
import re
import random
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from models import Endpoints

DEVELOPMENT_ENV = True
app = Flask(__name__)
api = Endpoints()

# Set token
api.ng_token = ""

# Select country
api.country = ""

# Create reference and user ids
api.reference_id = dt.now().strftime("%Y%m%d%H%M%S")
api.enduser_id = random.randint(10000, 99999)

@app.route('/', methods=['GET'])
def aspsps():
    """
    Query aspsp endpoint to get a list of all avialable ASPSPs (banks) in a given country.
    """

    if api.ng_token is None or api.ng_token == "":
        return render_template('select_missing_inputs.html', message="Missing token. Get a token from OB portal (ob.nordigen.com) and provide in app.py file.")
    if api.country is None or api.country == "":
        return render_template('select_missing_inputs.html', message="Missing country parameter. Provide two-letter country code (ISO 3166) in app.py file.")
    if api.reference_id is None or api.reference_id == "":
        return render_template('select_missing_inputs.html', message="Missing reference ID. Provide unique reference ID in app.py file.")
    if api.enduser_id is None or api.enduser_id == "":
        return render_template('select_missing_inputs.html', message="Missing end user ID. Provide end-user ID in app.py file.")

    banks = api.aspsps(api.country)
    banks = api.add_logo_link(banks)

    return render_template('select_aspsp.html', aspsps=banks)

@app.route('/<search>', methods=['GET'])
def aspsps_filtered(search):
    """
    Query aspsp endpoint to get a list of filtered ASPSPs (banks) in a given country.
    """

    banks = api.aspsps(api.country)
    banks = api.filter_aspsps(banks, search)
    banks = api.add_logo_link(banks)
    
    return render_template('select_aspsp.html', aspsps=banks)
        

@app.route('/agreements/<aspsp_id>', methods=['GET'])
def agreements(aspsp_id):
    """
    Logic from Quick start guide.

    Args:
        aspsp_id (str):  Unique identifier of the end users bank
    """
    if aspsp_id:
        # Create end user agreement
        api.enduser_agreement(aspsp_id)
        # Build a Link
        api.requisitions()
        # Create a redirect link
        redirect_url = api.requisition_link()
        # Redirect to aspsp
        return redirect(redirect_url)

    return redirect(url_for('index'))


@app.route('/results', methods=['GET'])
def results():
    """Nordigen redirects to this link. You should check reference ID if it matches."""
    ref_id = request.args.get('ref')

    if ref_id == api.reference_id:
        # Get account list
        all_accounts = api.accounts()
        # Get details, transactions & balances
        rersults = api.acc_data(all_accounts)
        return render_template('results.html', rersults=rersults, all_accounts=all_accounts)

    return "Reference error"


@app.route('/downloads/<filename>', methods=['GET', 'POST'])
def download(filename):
    """Download details, balances and transactions."""
    downloads = os.path.join(app.root_path, 'downloads')
    return send_from_directory(downloads, filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
