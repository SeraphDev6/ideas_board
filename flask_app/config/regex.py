import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
CAP_REGEX = re.compile(r'[A-Z]')
NUM_REGEX = re.compile(r'[0-9]')
SYM_REGEX = re.compile(r'[^a-zA-Z0-9]')
GITHUB_REGEX = re.compile(r"^https:\/\/github\.com\/")