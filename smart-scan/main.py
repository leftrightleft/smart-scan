# import os
import logging
import github
import sys


open_ai_key = sys.argv[0]
gh_token = sys.argv[1]
diff_url = sys.argv[2]


logging.info("Starting smart-scan")
logging.info(f"Diff URL: {diff_url}")

def main():
    gh = github.Client(gh_token)
    diff = gh.get_diff(diff_url)
    print(diff)

if __name__ == "__main__":
    main()
