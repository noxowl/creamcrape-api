import base64
import hashlib
import datetime

from packaging.version import Version, LegacyVersion, InvalidVersion
from flask import current_app

from .datahandler import packjson, packmsg


__all__ = ('pack', 'packjson', 'packmsg', 'status_code', 'make_credential', 'make_instant_id')


class StatusCode(object):
    success = 200
    bad_request = 400
    unauthorized = 401
    payment_required = 402
    forbidden = 403
    not_found = 404
    method_not_allowed = 405
    conflict = 409
    payload_too_large = 413

    precondition_required = 428


def pack(message):
    if current_app.config['DEBUG']:
        return packjson(message)
    return packmsg(message)


def make_credential(remote_address):
    id_hash = hashlib.sha512(remote_address.encode('utf-8'))
    return id_hash.hexdigest()


def make_instant_id(remote_address):
    from creamcrape.datehandler import begin_of_day
    bod = begin_of_day()
    id_hash = hashlib.sha512(
        '{0}:{1}'.format(
            remote_address,
            str(bod)
        ).encode('utf-8'),
    )
    return id_hash.hexdigest()[:16]


status_code = StatusCode()
