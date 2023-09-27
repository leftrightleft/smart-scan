# import os
import logging
import github
import sys
import openai


open_ai_key = sys.argv[0]
gh_token = sys.argv[1]
compare_url = sys.argv[2]


logging.info("Starting smart-scan")
logging.info(f"Diff URL: {compare_url}")

print(f"Diff URL: {compare_url}")
def main():
    gh = github.Client(gh_token)
    diff = gh.get_diff(compare_url + ".diff")
    print(diff)
    openai.organization = "org-SFRBhZ3jmlfD2tneIODU4iLZ"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.Model.list()

if __name__ == "__main__":
    main()
