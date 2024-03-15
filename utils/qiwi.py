import requests

from config import config


async def payment_history_last(my_login, api_access_token, rows_num, next_txn_id, next_txn_date):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_access_token
    parameters = {'rows': rows_num, 'nextTxnId': next_txn_id, 'nextTxnDate': next_txn_date}
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + my_login + '/payments', params=parameters)
    return h.json()


async def balance():
    s = requests.Session()
    s.headers['Accept'] = 'application/json'
    s.headers['authorization'] = 'Bearer ' + config("QIWI_TOKEN")
    b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + config("QIWI_ADDRESS") + '/accounts')
    return b.json()["accounts"][0]["balance"]["amount"]


async def check_payment(user_id, cost, balance_past):
    history = await payment_history_last(config("QIWI_ADDRESS"), config("QIWI_TOKEN"), "10", "", "")
    for i in range(8):
        if str(history['data'][i]['comment']) == str(user_id):
            print("comment - ok")
            if float(history["data"][i]["total"]["amount"]) >= float(cost):
                print("dengi - ok")
                if float(await balance()) > float(balance_past):
                    print("tyt toze - ok")
                    return True
