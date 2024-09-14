import BankOperations as bo
bank_accounts = {
1001: {
"first_name": "Alice",
"last_name": "Smith",
"id_number": "123456789",
"balance": 2500.50,
"transactions_to_execute": [
("2024-08-17 14:00:00", 1001, 1002, 300)],
"transaction_history": [
("2024-08-15 09:00:00", 1001, 1002, 500, "2024-08-15 09:30:00")]
},
1002: {
"first_name": "Bob",
"last_name": "Johnson",
"id_number": "987654321",
"balance": 3900.75,
"transactions_to_execute": [],
"transaction_history": [ ]
}}


def main():
    bo.interface(bank_accounts)


if __name__ == '__main__':
    main()

