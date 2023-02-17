from typing import List
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
def check_api_key(api_key, required_scopes):
    return {'test_key': 'test_value'}

def check_bearerAuth(token):
    return {'test_key': 'test_value'}


