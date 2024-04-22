import requests
from datetime import datetime
from flask import redirect, render_template, current_app, url_for, Blueprint, request

from . import utils as mu
from dcmain.config import Config
from dcmain.appstrings import ucl, ccl, lcl

mainapp = Blueprint('mainapp', __name__)

auth_header = {
    ccl.AUTHORIZATION: ""
}


@mainapp.route("/")
def home():

    ess = mu.get_route_essentials(auth_header)

    d = ess[lcl.params]

    dcp_data = requests.get(
        "{0}/api/v1/debts-credits/dc-profile/{1}/{2}/{3}/".format(
            ess[lcl.root_domain], d[lcl.user_id], d[lcl.password], d[lcl.dc_profile_id]
        ),
        headers=auth_header,
        timeout=1200,
    )

    dummy_dcp_data = {
        lcl.created_on: datetime.now(),
        lcl.timezone: "Africa/Lagos",
        lcl.created_via: ucl.API,
        lcl.id: "6477DCP68999",
        lcl.name: "DCP One",
        lcl.num_of_debtors: 5,
        lcl.num_of_creditors: 6,
        lcl.payables_and_receivables_d: {
            lcl.total_payables: 2000000,
            lcl.total_receivables: 1250000
        },
        lcl.primary_currency_d: {
            lcl.name: "Nigerian Naira",
            lcl.code: "566",
            lcl.symbol: "₦",
        }
    }

    return render_template("mainapp/home.html", title="Home", dcp_data=dcp_data.json() or dummy_dcp_data,
                           user_password=d[lcl.password], user_pin=d[lcl.pin])


@mainapp.route("/mainapp/create-debtor-creditor/", methods=['GET', 'POST'])
def create_debtor_or_creditor():

    name = request.form.get(lcl.name)
    creating = request.form.get(lcl.creating)
    user_pin = request.form.get(lcl.user_pin)
    user_password = request.form.get(lcl.user_password)

    if mu.is_eq(creating, ccl.DEBTOR):
        params = {lcl.creditor_dc_profile_id: request.form.get(
            lcl.creditor_dc_profile_id)}

    if mu.is_eq(creating, ccl.CREDITOR):
        params = {lcl.debtor_dc_profile_id: request.form.get(
            lcl.debtor_dc_profile_id)}

    ess = mu.get_route_essentials(auth_header)

    auth_header.update(ess[lcl.headers])

    params.update({
        lcl.name: name,
        lcl.user_pin: user_pin,
        lcl.user_password: user_password
    })

    d_or_c_data = requests.post(
        f"{ess[lcl.root_domain]}/api/v1/debts-credits/debtor/create/",
        headers=auth_header,
        timeout=1200,
        json=params,
    )

    print(params)
    print(d_or_c_data)
    print(d_or_c_data.text)

    return redirect(url_for('mainapp.home'))
