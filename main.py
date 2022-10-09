from email.mime import base
import requests
apiKey = '62305bcde5b70667020065dfb7392cb4'
baseURL = 'http://api.nessieisreal.com'


def main():
    radius = input("What radius do you want to search? (Miles): ")
    atms = get_ATMs(radius)
    print(
        f"There are {len(atms)} atms withing {radius} miles of Capital One's Headquarters!")


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


if __name__ == "__main__":
    main()
