
from dotenv import load_dotenv
from os import getenv

def load_safely(name):
    value = getenv(name)
    if not value:
        raise Exception(f"`{name}` variable not found!")
    return value

load_dotenv()

FINANCES_RENDER_SERVICE = load_safely('FINANCES_RENDER_SERVICE')
MAILGUN_BASE_URL = load_safely('MAILGUN_BASE_URL')
MAILGUN_KEY = load_safely('MAILGUN_KEY')
USER_EMAIL = load_safely('USER_EMAIL')
APP_EMAIL = load_safely('APP_EMAIL')
