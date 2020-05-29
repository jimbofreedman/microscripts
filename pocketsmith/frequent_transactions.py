import requests
import os

headers = {
    'accept': 'application/json',
    'x-developer-key': os.environ.get('POCKETSMITH_API_KEY')
}

def get(url):
    return requests.request("GET", url, headers=headers).json()

user_id = get("https://api.pocketsmith.com/v2/me")["id"]

transactions = []
page = 1

start = "2000-01-01"
end = "2030-01-01"

while True:
    print("Page", page)
    page_transactions = get(f"https://api.pocketsmith.com/v2/users/{user_id}/transactions?only_uncategorised=true&start_date={start}&end_date={end}&page={page}&per_page=100")

    if len(page_transactions) == 0 or not isinstance(page_transactions, list):
        break

    transactions = transactions + page_transactions
    page = page + 1

counts = {}
amounts = {}

for t in transactions:
    payee = t["payee"]
    if payee not in counts:
        counts[payee] = 1
        amounts[payee] = abs(t["amount"])
    else:
        counts[payee] = counts[payee] + 1
        amounts[payee] = amounts[payee] + abs(t["amount"])

sorted_counts = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}
sorted_amounts = {k: v for k, v in sorted(amounts.items(), key=lambda item: item[1])}


for x in sorted_amounts.items():
    print("%-30s\t\t\t%10d" % (x[0], x[1]))

for x in sorted_counts.items():
    print("%-30s\t\t\t%10d" % (x[0], x[1]))
