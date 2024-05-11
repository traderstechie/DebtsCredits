import json
import requests
from decimal import Decimal
from datetime import datetime, timezone
from flask import flash, redirect, render_template, url_for, Blueprint, request

from . import utils as mu
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

    return render_template("mainapp/home.html", dcp_data=dcp_data.json() or dummy_dcp_data,
                           title="Home", user_password=d[lcl.password], user_pin=d[lcl.pin],
                           root_domain=ess[lcl.root_domain], reversed=reversed)


@mainapp.route("/mainapp/create-debtor-creditor/", methods=['GET', 'POST'])
def create_debtor_or_creditor():

    name = request.form.get(lcl.name)
    creating = request.form.get(lcl.creating)
    user_pin = request.form.get(lcl.user_pin)
    user_password = request.form.get(lcl.user_password)

    if mu.is_eq(creating, lcl.debtor):
        params = {
            lcl.creditor_dc_profile_id: request.form.get(
                lcl.creditor_dc_profile_id)
        }

    if mu.is_eq(creating, lcl.creditor):
        params = {
            lcl.debtor_dc_profile_id: request.form.get(
                lcl.debtor_dc_profile_id)
        }

    ess = mu.get_route_essentials(auth_header)

    auth_header.update(ess[lcl.headers])

    params.update({
        lcl.name: name,
        lcl.user_pin: user_pin,
        lcl.user_password: user_password
    })

    req_res = requests.post(
        f"{ess[lcl.root_domain]}/api/v1/debts-credits/{creating}/create/",
        headers=auth_header,
        timeout=1200,
        json=params,
    )

    # print(params)
    # print(req_res)

    try:
        res_d = req_res.json() or json.loads(req_res.text)
    except ValueError:
        flash("Invalid/empty response received!", 'warning')
        return redirect(url_for('mainapp.home'))

    # print(res_d)

    if res_d.get(lcl.name) == name:
        # Success
        flash("New profile created successfully", 'success')
    elif res_d.get(lcl.status) == ccl.FAILURE:
        # Customer error
        flash("Operation failed with following messages:", 'info')
        for msg in res_d[lcl.errors]:
            flash(f"{msg}", 'warning')
    elif res_d.get(lcl.code):
        # Auto generated error
        flash("Operation failed with following messages:", 'info')
        for k, v in res_d.get(lcl.errors, {}).get(lcl.json, {}).items():
            flash(f"{k}: {v}", 'warning')
    else:
        flash("Unknown operation failure", 'info')

    return redirect(url_for('mainapp.home'))


@mainapp.route("/mainapp/create-debts-credits-txn/", methods=['GET', 'POST'])
def create_debts_credits_transaction():

    amount = request.form.get(lcl.amount)
    user_pin = request.form.get(lcl.user_pin)
    narration = request.form.get(lcl.narration)
    dc_profile_id = request.form.get(lcl.dc_profile_id)
    user_password = request.form.get(lcl.user_password)
    other_party_id = request.form.get(lcl.other_party_id)
    transaction_date = request.form.get(lcl.transaction_date)
    transaction_mode = request.form.get(lcl.transaction_mode)
    means_of_payment = request.form.get(lcl.means_of_payment)

    ess = mu.get_route_essentials(auth_header)

    auth_header.update(ess[lcl.headers])

    params = {
        lcl.amount: amount,
        lcl.user_pin: user_pin,
        lcl.narration: narration,
        lcl.user_password: user_password,
        lcl.dc_profile_id: dc_profile_id,
        lcl.other_party_id: other_party_id,
        lcl.transaction_mode: transaction_mode,
        lcl.means_of_payment: means_of_payment,
        lcl.transaction_date: transaction_date or datetime.now(timezone.utc).isoformat(),
    }

    req_res = requests.post(
        f"{ess[lcl.root_domain]}/api/v1/debts-credits/txn/create/",
        headers=auth_header,
        timeout=1200,
        json=params,
    )

    # print(params)
    # print(req_res)

    try:
        res_d = req_res.json() or json.loads(req_res.text)
    except ValueError:
        flash("Invalid/empty response received!", 'warning')
        return redirect(url_for('mainapp.home'))

    # print(res_d)

    if mu.is_valid_numeric(res_d.get(lcl.amount)) \
            and Decimal(res_d.get(lcl.amount)) == Decimal(amount or '0'):
        # Success
        flash("Transaction added successfully", 'success')
    elif res_d.get(lcl.status) == ccl.FAILURE:
        # Customer error
        flash("Operation failed with following messages:", 'info')
        for msg in res_d[lcl.errors]:
            flash(f"{msg}", 'warning')
    elif res_d.get(lcl.code):
        # Auto generated error
        flash("Operation failed with following messages:", 'info')
        for k, v in res_d.get(lcl.errors, {}).get(lcl.json, {}).items():
            flash(f"{k}: {v}", 'warning')
    else:
        flash("Unknown operation failure", 'info')

    return redirect(url_for('mainapp.home'))
