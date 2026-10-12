import secrets
from datetime import datetime


def GenerateOrderNumberService() -> str:
    """تولید شماره سفارش یکتا با فرمت BH-YYYYMMDD-XXXXXX"""
    date_part = datetime.now().strftime('%Y%m%d')
    random_part = ''.join(str(secrets.randbelow(10)) for _ in range(6))
    return f'BH-{date_part}-{random_part}'
