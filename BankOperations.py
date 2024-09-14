import datetime as dt


def get_action(action: str, accounts: dict):
    """
    This functions calls each function from the interface
    :param action:
    :param accounts:
    :return:
    """
    # Main interface actions
    if action == 'add':
        add_transaction(accounts)
    elif action == 'execute':
        execute_transactions(accounts)
    elif action == "reports":
        display_reports(accounts)

    # Reports' actions
    elif action == "all":
        print_all(accounts)
    elif action == "account":
        print_by_account(accounts)
    elif action == "id":
        print_by_id(accounts)
    elif action == "name":
        print_by_name(accounts)
    elif action == "ascending":
        print_balances_asc(accounts)
    elif action == "today":
        print_trans_today(accounts)
    elif action == "negatives":
        print_negative_balances(accounts)
    elif action == "total":
        print_total_balances(accounts)
    elif action == "adduser":
        fill_add_user(accounts)
    elif action == "alltrx":
        print_all_transactions(accounts)
    else:
        action = input("Enter a valid action ").lower()
        get_action(action, accounts)


def print_all(accounts: dict):
    """
    Prints all accounts
    :param accounts:
    :return:
    """
    print(accounts, end='\n\n')


def print_by_account(accounts: dict):
    """
    Prints account by its account number
    :param accounts:
    :return:
    """
    account = account_valid(accounts)
    print(accounts[account], end='\n\n')


def print_by_id(accounts: dict):
    """
    Prints account by user id
    :param accounts:
    :return:
    """
    account_id = str(amount_valid())[0:-2]
    for i in accounts:
        if accounts[i]["id_number"] == account_id:
            print(f'{i} : {accounts[i]}', end='\n\n')
    return


def print_balances_asc(accounts: dict):
    """
        Prints all balances in ascending order
        :param accounts:
        :return:
        """
    sorted_accounts = sorted(accounts.values(), key=lambda x: x['balance'])
    print(sorted_accounts, end="\n\n")


def print_by_name(accounts: dict):
    """
            Prints account by user name
            :param accounts:
            :return:
            """
    account_name = input("Enter the users' first name ").lower()
    for i in accounts:
        if account_name in accounts[i]["first_name"].lower():
            print(f'{i} : {accounts[i]}', end="\n\n")
    return


def print_trans_today(accounts: dict):
    """
            Prints all the transactions that occurred today
            :param accounts:
            :return:
            """
    now = dt.datetime.now()
    now_formated = now.strftime('%Y-%m-%d')
    trans: list = []
    for i in accounts:
        if accounts[i]['transaction_history']:
            trans.append(accounts[i]['transaction_history'])
    trans_today: list = []
    for i in trans:
        date_extract = i[0][4][:-9]
        if date_extract == now_formated:
            trans_today.append(i)
    print(trans_today, end="\n\n")


def print_negative_balances(accounts: dict):
    """
            Prints all accounts with negative balance
            :param accounts:
            :return:
            """
    negatives: list = []
    for i in accounts:
        if accounts[i]['balance'] < 0:
            negatives.append(accounts[i])
    if negatives:
        print(negatives, end="\n\n")
    else:
        print("No account with a negative balance, somehow...", end="\n\n")


# Bonus
def print_all_transactions(accounts: dict):
    """
            Prints the transactions that were executed, sorted by date
            :param accounts:
            :return:
            """
    trx = []
    for i in accounts:
        for j in accounts[i]['transaction_history']:
            trx.append(j)
    trx_sorted = sorted(trx, key=lambda x: x[4], reverse=True)
    print(trx_sorted)


def print_total_balances(accounts: dict):
    """
            Prints all balances combined
            :param accounts:
            :return:
            """
    balances = 0.0
    for i in accounts:
        balances += accounts[i]['balance']
    print(balances, end='\n\n')


def fill_add_user(accounts: dict):
    """
                Fills the add user function
                :param accounts:
                :return:
                """
    # Bonus

    fn = input("Enter the users' first name ")
    ln = input("Enter the users' last name ")
    print("Now the id number ")
    idn = str(amount_valid())
    while True:
        try:
            balance = float(input("Enter the users' balance "))
            break
        except:
            print("Enter a valid number ")
    add_user(accounts, fn, ln, idn, balance)
    print("User added successfully! ", end="\n\n")


def add_user(accounts: dict, first_name: str, last_name: str, id_number: str
             , balance: float):
    """
                Adds a new user
                :param accounts:
                :return:
                """
    unique_key = list(accounts.keys())[-1] + 1
    return accounts.update({unique_key: {
        "first_name": first_name,
        "last_name": last_name,
        "id_number": id_number,
        "balance": balance,
        "transactions_to_execute": [],
        "transaction_history": []
    }})


def account_valid(accounts: dict):
    """
                Checks if the account exists
                :param accounts:
                :return:
                """
    while True:
        try:
            account = int(input("Enter an account number"))
            if accounts.get(account, False):
                return account
            else:
                print("This account doesn't exist")
        except:
            print("Enter an integer")


def amount_valid():
    """
                Checks if the amount is valid
                :param accounts:
                :return:
                """
    while True:
        try:
            amount = float(input("Enter amount/number "))
            if amount > 0:
                return amount
            else:
                print("Enter a number bigger than zero")
        except:
            print("Enter a valid number")


def add_transaction(accounts):
    """
                Adds a new transaction
                :param accounts:
                :return:
                """
    original = 0
    receiving = 0
    amount = 0
    print("The paying account...")
    original = account_valid(accounts)
    print("The receiving account...")
    receiving = account_valid(accounts)
    amount = amount_valid()
    print("Transaction added successfully!\n")
    now = dt.datetime.now()
    transaction_date = now.strftime('%Y-%m-%d %H:%M:%S')
    accounts[original]['transactions_to_execute'].append((transaction_date, original, receiving, amount))


def execute_transactions(accounts: dict):
    """
                Execute all transactions by account
                :param accounts:
                :return:
                """
    account = account_valid(accounts)
    if accounts[account]["transactions_to_execute"]:
        now = dt.datetime.now()
        transaction_date = now.strftime('%Y-%m-%d %H:%M:%S')
        for i in accounts[account]['transactions_to_execute']:
            accounts[i[1]]['balance'] -= i[3]
            accounts[i[2]]['balance'] += i[3]
            accounts[account]['transaction_history'].append((i + (transaction_date,)))
        accounts[account]['transactions_to_execute'].clear()
        print(accounts[account])
        print("Transactions executed successfully!\n")
    else:
        print("This account has no transactions\n")


def display_reports(accounts: dict):
    """
                Displays reports
                :param accounts:
                :return:
                """
    print("This is the reports interface")
    print("In order to perform any action write the wanted action like so...")
    while True:
        print('"All" - print all of the accounts, "Account" - print account'
              ' by account number, "Id" - print account by the users id number, '
              '"Name" - print account by first name, "Ascending" - prints '
              f'the accounts{"'"} balance in an ascending order,"Today" - print all the transactions'
              f'that were executed today, "Negatives" - print all the accounts with negative balance, '
              f'"Total - print all of the balances{"'"} combined value, '
              f'"AddUser - add a user to the bank accounts'
              f'"AllTrx" - print all of the transactions that were executed in the bank,'
              f' sorted by date'
              f', "Exit" - exits to main interface ')
        action = input("Enter an action ").lower()
        if action == 'exit':
            return
        else:
            get_action(action, accounts)


def interface(accounts: dict):
    """
                Display the main interface
                :param accounts:
                :return:
                """
    print("Welcome to the Rothschild central bank!")
    print("In order to perform any action write the wanted action like so...")
    while True:
        print('"Add" - add a new transaction, "Execute" - executing all existing transactions, '
              '"Reports" - enter the reports interface, "Exit" - '
              'exit the banks system')
        action = input("Enter action ").lower()
        if action == 'exit':
            print("Bye bye ! ")
            break
        else:
            get_action(action, accounts)


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
        "transaction_history": [("2024-08-15 09:00:00", 1002, 1001, 500, "2024-09-13 09:55:00")]
    },
    1003: {
        "first_name": "Bob",
        "last_name": "Johnson",
        "id_number": "987654321",
        "balance": -1700.75,
        "transactions_to_execute": [],
        "transaction_history": [("2024-08-15 09:00:00", 1003, 1002, 500, "2024-09-13 09:30:00")]
    }}
print()
add_user(bank_accounts, "Carl", "Turner", "567894321", 5324)
interface(bank_accounts)
