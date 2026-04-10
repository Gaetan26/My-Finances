
from datetime import datetime

def format_date_now():
    return datetime.now().strftime('%Y/%m/%d')

def format_time_now():
    return datetime.now().strftime('%H:%M')
