"""Flask app."""
from datetime import datetime as dt
import os
import re
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from models import Endpoints

DEVELOPMENT_ENV = True
app = Flask(__name__)
api = Endpoints()


@app.route('/')
def index():
    """Index page - Token form."""
    return render_template('get_token.html')


@app.route('/', methods=['POST'])
def my_form_post():
    """Get Nordigen access tokken. Copy from the Nordigen's Open Banking Portal."""
    input_string = request.form['text']
    ng_token = re.sub('[^A-Za-z0-9]+', '', input_string)

    if ng_token:
        # Set token
        api.ng_token = ng_token

        # Create reference and user ids
        api.reference_id = dt.now().strftime("%Y%m%d%H%M%S")
        api.enduser_id = 666
        return redirect(url_for('countries'))

    return redirect(url_for('index'))


@app.route('/select-contry', methods=['GET'])
def countries():
    """Create list of countries to chose from."""
    if api.ng_token:
        return render_template(
                'select_country.html', contries=['AT', 'BE', 'EE', 'FI', 'IE', 'LV', 'LT']
            )

    return redirect(url_for('index'))


@app.route('/select-aspsp/<country>', methods=['GET'])
def aspsps(country):
    """
    Query aspsp endpoint to get a list of all avialable ASPSPs (banks) in a given country.

    Args:
        country (str): Two-character country code
    """
    if country:
        banks = api.aspsps(country)
        return render_template('select_aspsp.html', aspsps=banks)

    return redirect(url_for('index'))


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
        # Get transactions & balances
        rersults = api.acc_data(all_accounts)
        return render_template('results.html', rersults=rersults, all_accounts=all_accounts)

    return "Reference error"


@app.route('/downloads/<filename>', methods=['GET', 'POST'])
def download(filename):
    """Download balances and transactions."""
    downloads = os.path.join(app.root_path, 'downloads')
    return send_from_directory(directory=downloads, filename=filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
