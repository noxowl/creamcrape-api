import base64
import hashlib

__all__ = ('make_credential', 'make_instant_id')


def make_credential(remote_address):
    id_hash = hashlib.sha512(remote_address)
    return base64.urlsafe_b64encode(id_hash.digest())


def make_instant_id(remote_address):
    from creamcrape.datehandler import begin_of_day
    bod = begin_of_day()
    id_hash = hashlib.sha512(
        '{0}:{1}'.format(
            remote_address,
            str(bod)
        ),
    )
    return base64.urlsafe_b64encode(id_hash.digest()[:10])

