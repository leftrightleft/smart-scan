# import os
import logging
import requests
import sys

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)

open_ai_key = sys.argv[0]
gh_token = sys.argv[1]
diff_url = sys.argv[2]

class Client:
    def __init__(self, token):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }

    def get_diff(client, compare_url):
        response = requests.get(compare_url + ".diff", headers=client.headers)
        if response.status_code == 200:
            logging.info("Successfully retrieved diff")
            return response.text
        else:
            e = f"Error retrieving diff.  Response: {response.json()}"
            logging.error(e)
            raise Exception(e)
        
print(f"Open AI Key: {open_ai_key}")
print(f"Diff URL: {diff_url}")

def main():
    client = Client(open_ai_key)
    diff = client.get_diff(diff_url)
    print(diff)

if __name__ == "__main__":
    main()
