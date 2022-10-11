from random import randint
import names
import requests
apiKey = 'API KEY GOES HERE'
baseURL = 'http://api.nessieisreal.com'


def main():
    radius = input("What radius do you want to search? (Miles): ")
    atms = get_ATMs(radius)
    print(
        f"There are {len(atms)} atms withing {radius} miles of Capital One's Headquarters!")

    should_create_new_customer = input(
        "Do you want to create a new customer? (y/n): ").upper() == 'Y'
    if (should_create_new_customer):
        customer = {
            "first_name": names.get_first_name(),
            "last_name": names.get_last_name(),
            "address": {
                "street_number": str(random_with_N_digits(5)),
                "street_name": f'{names.get_first_name()} street',
                "city": "Chapel Hill",
                "state": "NC",
                "zip": "27514"
            }
        }
        customer_creation = create_customer(customer)
        print(
            f'{customer_creation["message"]}: {customer_creation["objectCreated"]} \n')

    should_get_all_customers = input(
        "Do you want to retrieve all customers? (y/n): ").upper() == 'Y'
    if (should_get_all_customers):
        all_customers = get_all_customers()
        print(f'Retrieved the following customers: \n {all_customers}')

    should_get_all_accounts = input(
        "Do you want to retrieve all customers and create a  new account for each? (y/n): ").upper() == "Y"
    if (should_get_all_accounts):
        created_accounts = create_accounts(all_customers)
        print(f'\nCreated accounts: \n{created_accounts}')

    should_add_bill_all_accounts = input(
        "Do you want to retrieve all accounts and create a new bill for each? (y/n): ").upper() == "Y"
    if (should_add_bill_all_accounts):
        account_ids = get_all_accounts()
        print(f'Retrieved following accounts: \n{account_ids}')
        bills_response = add_bill_to_accounts(account_ids)
        if bills_response:
            print("\nAdded $100.00 bill to each account!")

    should_make_purchase = input(
        "Do you want to make a payment? (y/n): ").upper() == "Y"
    if (should_make_purchase):
        account_id = input(
            "What account? (Example: 63448a4078f6910a15f0b83f): ")
        ammount = input("How much $? (Example: 100): ")
        payment_respose = make_purchase(account_id, ammount)
        print(payment_respose)

    should_make_withdrawal = input(
        "Do you want to make a withdrawal? (y/n): ").upper() == "Y"
    if (should_make_withdrawal):
        account_id = input(
            "What account? (Example: 63448a4078f6910a15f0b83f): ")
        ammount = input("How much $? (Example: 100): ")
        withdrawal_response = make_withdrawal(account_id, ammount)
        print(withdrawal_response)

    should_delete_all_accounts = input(
        "Do you want to delete all customers ? (y/n): ").upper() == "Y"
    if (should_delete_all_accounts):

        delete_response = delete_all("Customers")
        print(f'Delete response: {delete_response}')
    should_delete_all_accounts = input(
        "Do you want to delete all accounts ? (y/n): ").upper() == "Y"
    if (should_delete_all_accounts):

        delete_response = delete_all("Accounts")
        print(f'Delete response: {delete_response}')
    should_fetch_all_bills = input(
        "Do you want to fetch all enterprise bills ? (y/n): ").upper() == "Y"
    if (should_fetch_all_bills):
        bills = get_enterprise_all_bills()
        print(
            f"Here are the payees for the first 5 bills from the enterprise: \n {bills[:5]}")


def get_ATMs(radius):
    MAX_PAGES = 100
    LATTITUDE = 38.9259742
    LONGITUDE = -77.2143267
    atms = []
    endpoint = f'{baseURL}/atms?lat={LATTITUDE}&lng={LONGITUDE}&rad={radius}&key={apiKey}&page=1'
    for _ in range(MAX_PAGES):
        response = requests.get(
            url=endpoint,
            headers={'content-type': 'application/json'},
        ).json()
        data = response["data"]
        if not data:
            return atms
        for atm in data:
            atms.append(atm["name"])
        endpoint = f'{baseURL}{response["paging"]["next"]}'


def create_customer(customer):
    endpoint = f'{baseURL}/customers?key={apiKey}'
    customer_response = requests.post(endpoint, json=customer).json()
    if customer_response["code"] == 201:
        return customer_response
    else:
        raise Exception()


def get_all_customers():
    endpoint = f'{baseURL}/customers?key={apiKey}'
    customers_response = requests.get(endpoint).json()
    ids = []
    for customer in customers_response:
        ids.append(customer["_id"])
    return ids


def create_accounts(ids):
    account_ids = []
    for id in ids:
        endpoint = f'{baseURL}/customers/{id}/accounts?key={apiKey}'
        json_data = {
            'type': 'Credit Card',
            'nickname': 'string',
            'rewards': 100,
            'balance': 100,
            'account_number': str(random_with_N_digits(16)),
        }
        create_accounts_response = requests.post(
            endpoint, json=json_data).json()
        account_ids.append(create_accounts_response["objectCreated"]["_id"])
    return account_ids


def get_all_accounts():
    ids = []
    endpoint = f'{baseURL}/accounts?key={apiKey}'
    accounts_response = requests.get(endpoint).json()
    for account in accounts_response:
        ids.append(account["_id"])
    return ids


def delete_all(type):
    endpoint = f'{baseURL}/data?type={type}&key={apiKey}'
    delete_response = requests.delete(endpoint)
    return (delete_response)


def add_bill_to_accounts(account_ids):
    for id in account_ids:
        endpoint = f'{baseURL}/accounts/{id}/bills?key={apiKey}'
        json_data = {
            'status': 'pending',
            'payee': 'Payee',
            'nickname': 'Demo Payment',
            'payment_date': '2022-10-10',
            'recurring_date': 10,
            'payment_amount': 100,
        }
        add_bills_response = requests.post(
            endpoint, json=json_data).json()
        if add_bills_response["code"] != 201:
            return False
    return True


def make_purchase(id, amount):
    endpoint = f'{baseURL}/accounts/{id}/purchases?key={apiKey}'
    json_data = {
        "merchant_id": "63458f4d78f6910a15f0bd0c",
        "medium": "balance",
        "purchase_date": "2022-10-11",
        "amount": int(amount),
        "status": "pending",
        "description": "payment to UNC"
    }
    try:
        return requests.post(endpoint, json=json_data).json()
    except:
        return "Invalid ID"


def make_withdrawal(id, amount):
    endpoint = f'{baseURL}/accounts/{id}/withdrawals?key={apiKey}'
    json_data = {
        "medium": "balance",
        "transaction_date": "2022-10-11",
        "status": "pending",
        "amount": int(amount),
        "description": "string"
    }
    try:
        return requests.post(endpoint, json=json_data).json()
    except:
        return "Invalid ID"


def get_enterprise_all_bills():
    endpoint = f'{baseURL}/enterprise/bills?key={apiKey}'
    bills = []
    all_bills_response = requests.get(endpoint).json()
    for bill in all_bills_response["results"]:
        bills.append(bill["payee"])
    return bills


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


if __name__ == "__main__":
    main()
