import pytest
import datetime as dt
import copy

bank_accounts = {
1001: {
"first_name": "Alice",
"id_number": "123456789",
"balance": 2500.50,
"transactions_to_execute": [
("2024-08-17 14:00:00", 1001, 1002, 300), ("2024-08-17 15:00:00", 1001, 1002, 200)],
"transaction_history": [
("2024-08-15 09:00:00", 1001, 1002, 500, "2024-08-15 09:30:00") ]
},
1002: {
"first_name": "Bob",
"last_name": "Johnson",
"id_number": "987654321",
"balance": 3900.75,
"transactions_to_execute": [],
"transaction_history": [ ]
},
1003: {
"first_name": "Ali",
"last_name": "Hamdan",
"id_number": "987654321",
"balance": 3900.75,
"transactions_to_execute": [],
"transaction_history": [ ]
}}


def perform_trx(account: int, accounts: dict):
    if accounts[account]["transactions_to_execute"]:
        now = dt.datetime.now()
        transaction_date = now.strftime('%Y-%m-%d %H:%M:%S')
        for i in accounts[account]['transactions_to_execute']:
            accounts[i[1]]['balance'] -= i[3]
            accounts[i[2]]['balance'] += i[3]
            accounts[account]['transaction_history'].append((i + (transaction_date,)))
        accounts[account]['transactions_to_execute'].clear()


def create_trx(accounts: dict, original: int, receiving: int, amount: float):
    now = dt.datetime.now()
    transaction_date = now.strftime('%Y-%m-%d %H:%M:%S')
    accounts[original]['transactions_to_execute'].append((transaction_date, original, receiving, amount))


def get_by_name(accounts: dict, first_name: str):
    valids = []
    for i in accounts:
        if first_name.lower() in accounts[i]["first_name"].lower():
            valids.append(i)
    return valids


def test_trx_empty():
    accounts = copy.deepcopy(bank_accounts)
    perform_trx(1001, accounts)
    assert accounts[1001]['transactions_to_execute'] == []


def test_added_history():
    accounts = copy.deepcopy(bank_accounts)
    trx = accounts[1001]['transactions_to_execute'][:]
    perform_trx(1001, accounts)
    trx_count = len(trx)
    matched_count = 0
    for original_trx in trx:
        matched = any(
            original_trx == hist_trx[:4]
            for hist_trx in accounts[1001]["transaction_history"]
        )
        if matched:
            matched_count += 1
    assert trx_count == matched_count


def test_balance_decreased():
    accounts = copy.deepcopy(bank_accounts)
    amount = 0
    former_balance = accounts[1001]['balance']
    for i in accounts[1001]['transactions_to_execute']:
        amount += i[3]
    perform_trx(1001, accounts)
    assert former_balance - amount == accounts[1001]['balance']


def test_balance_increased():
    accounts = copy.deepcopy(bank_accounts)
    amount = 0
    former_balance = accounts[1002]['balance']
    for i in accounts[1001]['transactions_to_execute']:
        amount += i[3]
    perform_trx(1001, accounts)
    assert former_balance + amount == accounts[1002]['balance']


def test_added_trx():
    # Bonus included
    accounts = copy.deepcopy(bank_accounts)
    now = dt.datetime.now()
    transaction_date = now.strftime('%Y-%m-%d %H:%M:%S')
    trx = (transaction_date, 1001, 1002, 999)
    create_trx(accounts, 1001, 1002, 999)
    assert trx in accounts[1001]['transactions_to_execute']


def test_first_names():
    accounts = copy.deepcopy(bank_accounts)
    valids = get_by_name(accounts, 'ali')
    assert valids == [1001, 1003]
