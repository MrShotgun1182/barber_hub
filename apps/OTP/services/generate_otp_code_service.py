import secrets

def GenerateOTPCodeService(length: int = 6) -> str:
    """تولید کد یکبار مصرف عددی ۶ رقمی"""
    return "".join([str(secrets.randbelow(10)) for _ in range(length)])