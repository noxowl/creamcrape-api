from marshmallow import fields
from sqlalchemy.schema import Column, ForeignKey, Index
from sqlalchemy.sql.functions import now
from sqlalchemy.dialects import mysql
from sqlalchemy.types import (DateTime, Integer, SmallInteger, BigInteger,
                              String, Boolean, JSON, UnicodeText)

__all__ = ('UserDataMixin', 'DateTimeMixin', 'UserDataSchemaMixin', 'DateTimeSchemaMixin')


class UserDataSchemaMixin(object):
    username = fields.Str()
    email = fields.Str()
    user_instant_id = fields.Str()


class DateTimeSchemaMixin(object):
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class UserDataMixin(object):
    username = Column(String, nullable=False, default='')
    email = Column(String, nullable=False, default='')
    user_instant_id = Column(String, nullable=False, default='')
    user_credential = Column(String, nullable=False, default='')


class DateTimeMixin(object):
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
