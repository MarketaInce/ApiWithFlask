"""
SECURITY
"""

from werkzeug.security import safe_str_cmp
from code.earlier_sections.section_5 import User


def authenticate(username, password):
    """

    :param username:
    :param password:
    :return:
    """
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    """

    :param payload:
    :return:
    """
    user_id = payload['identity']
    return User.find_by_id(user_id)
