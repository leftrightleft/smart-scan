# import os
import logging
import github
import sys
import openai


logging.basicConfig(filename="logging.log", level=logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)

open_ai_key = sys.argv[1]
gh_token = sys.argv[2]
compare_url = sys.argv[3]


logging.info("Starting smart-scan")
logging.info(f"Diff URL: {compare_url}")


def main():
    gh = github.Client(gh_token)
    diff = gh.get_diff(compare_url + ".diff")
    logging.info(f"Diff: {diff}")
    openai.organization = "org-SFRBhZ3jmlfD2tneIODU4iLZ"
    openai.api_key = open_ai_key
    models = openai.Model.list()
    logging.info(f"Models: {models}")
    

if __name__ == "__main__":
    main()
