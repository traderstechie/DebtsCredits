import os
import requests
from flask import render_template, current_app
from datetime import datetime

from dcmain.config import Config
from dcmain.appstrings import ucl, ccl, lcl

auth_header = {
    ccl.AUTHORIZATION: ""
}


def home():

    # r = requests.get("https://tradepally.com", timeout=1200)
    # print(r.status_code)
    # print(r.headers)
    # print(r.text)
    # print(":::::::::::")
    # # print(r.json())

    # post_data = {
    #     "first_name": "Chimeziri",
    #     "last_name": "Obioha",
    #     "phone": "09090909090",
    #     "country": "Nigeria",
    #     "dial_code": "+234",
    #     "email": "email@email.com",
    #     "password": "nfere1866"
    # }
    # r = requests.post(
    #     "https://tradepally.com/api/v1/users/create/",
    #     headers=auth_header,
    #     json=post_data,
    #     timeout=1200,
    # )
    # print(r.status_code)
    # print(r.headers)
    # print(r.text)

    get_dcp_params = {
        lcl.development: {
            lcl.user_id: "1088823636",
            lcl.dc_profile_id: "3505DCP36219811",
            lcl.password: os.environ.get(ucl.TP_DEV_PASSWORD),
        },
        lcl.production: {
            lcl.password: "test1234",
            lcl.user_id: "1045236820",
            lcl.dc_profile_id: "4103DCP20256990",
        },
    }

    if current_app.config.get(ucl.PRODUCTION_ENV):
        d = get_dcp_params[lcl.production]

        root_domain = "https://tradepally.com"

        auth_header.update(
            {ccl.AUTHORIZATION: Config.TRADEPALLY_PRODUCTION_API_AUTH_TOKEN})
    else:
        d = get_dcp_params[lcl.development]

        root_domain = "http://localhost:5000"

        auth_header.update(
            {ccl.AUTHORIZATION: Config.TRADEPALLY_LOCALHOST_API_AUTH_TOKEN})

    print(f"::::::::{current_app.root_path}::::::::")

    dcp_data = requests.get(
        # f"https://tradepally.com/api/v1/debts-credits/dc-profile/"
        # f"{d[lcl.user_id]}/{d[lcl.password]}/{d[lcl.dc_profile_id]}/",
        "{0}/api/v1/debts-credits/dc-profile/{1}/{2}/{3}/".format(
            root_domain, d[lcl.user_id], d[lcl.password], d[lcl.dc_profile_id]
        ),
        # params=get_dcp_params[lcl.production],
        headers=auth_header,
        timeout=1200,
    )

    # {
    #     "name": "Test API DC Profile",
    #     "currency_numeric": "566",
    #     "timezone": "Africa/Lagos",
    #     "user_id": "1045236820",
    #     "user_password": "test1234",
    #     "user_pin": "string"
    # }

    # {
    #     "created_on": "2024-03-25T07:54:53.276910+00:00",
    #     "id": "4103DCP20256990",
    #     "name": "Test API DC Profile",
    #     "primary_currency_d": {
    #         "code": "NGN",
    #         "name": "Naira",
    #         "symbol": "₦"
    #     },
    #     "timezone": "Africa/Lagos"
    # }

    print(f"::::::::::::{dcp_data.url}::::::::::::::::")
    print(f"::::::::::::{dcp_data.status_code}::::::::::::::::")
    print(
        f"::::::::::::{os.environ.get(ucl.TRADEPALLY_LOCALHOST_API_AUTH_TOKEN)}::::::::::::::::")
    print(f"::::::::::::{dcp_data.json()}::::::::::::::::")

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

    return render_template("home.html", title="Home", dcp_data=dcp_data.json() or dummy_dcp_data)
