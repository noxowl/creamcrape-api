import json
import base64
import msgpack
import datetime


__all__ = ('packjson', 'packmsg', 'to_msgpack', 'from_msgpack')


def decode_datetime(obj):
    if '__datetime__' in obj:
        obj = datetime.datetime.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S.%f")
    return obj


def encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
    return obj


def packjson(message):
    return json.dumps(message, ensure_ascii=False, indent=4)


def packmsg(message):
    return base64.encodebytes(msgpack.packb(message, use_bin_type=True))


def to_msgpack(data, **kwargs):
    if 'ext' in kwargs:
        if 'datetime' in kwargs['ext']:
            return msgpack.packb(data, default=encode_datetime, use_bin_type=True)
    return msgpack.packb(data, use_bin_type=True)


def from_msgpack(data, **kwargs):
    if 'ext' in kwargs:
        if 'datetime' in kwargs['ext']:
            return msgpack.unpackb(data, object_hook=decode_datetime, raw=False)
    return msgpack.unpackb(data, raw=False)


def is_odd(num):
    if num % 2 == 0:
        return False
    else:
        return True


def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False
