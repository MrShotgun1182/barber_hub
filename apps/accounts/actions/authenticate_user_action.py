from typing import Dict, Any
from accounts.services.authenticate_user_service import AuthenticateUserService


def AuthenticateUserAction(username: str, password: str) -> Dict[str, Any]:
    """
    اکشن بررسی صحت اطلاعات ورود و استخراج نقش کاربر
    """
    user = AuthenticateUserService(username=username, password=password)

    if user is not None:
        return {
            "is_authenticated": True,
            "role": user.role
        }

    return {
        "is_authenticated": False,
        "role": None
    }