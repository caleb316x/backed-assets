import requests
import json
from tabulate import tabulate
import time
from envCheck import load_and_validate_env
import os

class Bot:

    def __init__(self):   
        self.chain = os.getenv("chain")
        self.url = "https://"+self.chain+".api.atomicassets.io/atomicmarket/v2/sales"
        self.max_page = int(os.getenv("max_page"))
        self.start_page = int(os.getenv("start_page"))
        self.sleep = 1
        self.backed_count = 0
        self.asset_per_page = int(os.getenv("asset_per_page"))
        self.page_count = 0
        self.asset_count = 0
        self.last_page = self.start_page
        self.order = os.getenv("order")
        self.collections = os.getenv("collections")

        self.params = {
            'page': 1,
            'limit': self.asset_per_page,
            'order': self.order,
            'sort': 'created',
            'state': 1,
            'collection_name': ",".join(self.collections),
        }

        self.rows = []
        self.alldata = []
        self.assets_buy = []

    def getName(self, asset):
        try:
            return asset["data"]["name"]
        except KeyError:
            try:
                return asset["name"]
            except KeyError:
                return " ***** no name *****"

    def search_assets(self, page):
        print("page: " + str(page))
        self.params['page'] = page

        response = requests.get(self.url, params=self.params)

        if response.status_code == 200:
            self.page_count += 1
            data = response.json()
            self.last_page = page
            for d in data["data"]:
                precision_factor = 10 ** d["price"]['token_precision']

                self.asset_count += len(d["assets"])
                price = int(d["price"]['amount']) / precision_factor
                sale_id = d["sale_id"]

                for asset in d["assets"]:
                    asset_id = asset["asset_id"]
                    collection_name = asset["collection"]["collection_name"]
                    bundle = "🔒 " if len(d["assets"]) > 1 else ""
                    name = bundle + self.getName(asset)

                    backed_total = 0
                    for b in asset["backed_tokens"]:
                        backed_total += b['amount'] / precision_factor

                    backed = backed_total
                    suggested_median = 0
                    suggested_average = 0
                    if "prices" in asset:
                        if len(asset['prices']) > 0:
                            suggested_median = int(asset['prices'][0]['suggested_median']) / precision_factor
                            suggested_average = int(asset['prices'][0]['suggested_average']) / precision_factor

                    buy = "❌"
                    if backed >= price:
                        buy = "✅"
                        self.assets_buy.append([sale_id, name, collection_name, price, suggested_median, suggested_average, backed, buy])
                    elif backed != 0:
                        self.assets_buy.append([sale_id, name, collection_name, price, suggested_median, suggested_average, backed, buy])
                        

                    self.rows.append([sale_id, name, collection_name, price, suggested_median, suggested_average, backed])

            self.alldata.append(data["data"])

            if len(data["data"]) < self.asset_per_page:
                return False

            return True
        else:
            print(f"Request failed with status code {response.status_code}")
            return False

    def getAssets(self):
        print("Chain: "+self.chain)
        for p in range(self.start_page, self.max_page + 1):
            res = self.search_assets(p)
            time.sleep(self.sleep)

            if not res:
                break

        headers = ["ID", "Name", "Collection", "price", "median", "average", "backed"]
        print(tabulate(self.rows, headers=headers, tablefmt='grid'))

        print("=============BUY=============")
        headers = ["ID", "Name", "Collection", "price", "median", "average", "backed", "buy"]
        print(tabulate(self.assets_buy, headers=headers, tablefmt='grid'))

        print("Backed assets: " + str(self.backed_count))
        print("---------------------------")
        print("total assets: " + str(self.asset_count))
        print("total pages: " + str(self.page_count))

        with open("data.json", 'w') as json_file:
            json.dump(self.alldata, json_file, indent=4)


if __name__ == "__main__":
    envdata = load_and_validate_env('.env')
    if(envdata):
        bot = Bot()
        bot.getAssets()

# https://eos.atomichub.io/market/sale/eos-mainnet/sale_id_here
# https://eos.atomichub.io/explorer/asset/eos-mainnet/asset_id_here
