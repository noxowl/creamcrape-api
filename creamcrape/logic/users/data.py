from marshmallow import Schema, fields
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.schema import Column, ForeignKey, Index
from sqlalchemy.types import (DateTime, Integer, SmallInteger, BigInteger,
                              String, Boolean, JSON, UnicodeText)

from creamcrape.db.orm import Base

__all__ = ('User', 'AuthorizedUser')


class UserSchema(Schema):
    instant_id = fields.Str()


class User(object):
    __tablename__ = 'user'

    username = Column(String)
    email = Column(String)
    credential = Column(String)

    def set(self, **kwargs):
        self.username = kwargs['username'] if 'username' in kwargs else ''
        self.email = kwargs['email'] if 'email' in kwargs else ''

    def set_credential(self, remote_address):
        from creamcrape.common import make_credential
        self.credential = make_credential(remote_address)

    @property
    def instant_id(self):
        if hasattr(self, '_instant_id'):
            return self._instant_id
        else:
            from creamcrape.common import make_instant_id
            _instant_id = make_instant_id(self.credential)
            setattr(self, '_instant_id', _instant_id)
            return _instant_id


class AuthorizedUser(User, Base):
    __tablename__ = 'authorized_user'

    id = Column(BigInteger, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime)
