import random

def GenerateOTPCodeService(length: int = 5) -> str:
    """تولید کد یکبار مصرف عددی"""
    return "".join([str(random.randint(0, 9)) for _ in range(length)])