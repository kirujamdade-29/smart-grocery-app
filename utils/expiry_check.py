from datetime import datetime

def check_expiry(items):
    today = datetime.today().date()
    for item in items:
        expiry_date = datetime.strptime(item['expiry'], '%Y-%m-%d').date()
        item['expired'] = expiry_date < today
