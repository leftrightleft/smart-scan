import logging
import sys

# Set up logging to file
logging.basicConfig(filename="bootcamp-setup.log", level=logging.INFO)

# Set up logging to console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)