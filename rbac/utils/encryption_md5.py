import hashlib
from django.conf import settings


def encryption_str(origin):
    """
    md5
    :param origin:
    :return:
    """
    secret_key = settings.SECRET_KEY
    ha = hashlib.md5(str.encode(secret_key))
    ha.update(origin.encode('utf-8'))
    return ha.hexdigest()
