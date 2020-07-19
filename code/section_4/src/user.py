"""
USER |
"""


class User:
    """
    A proper user Class that stores
    1. User ID
    2. User Name
    3. User Password
    """
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password