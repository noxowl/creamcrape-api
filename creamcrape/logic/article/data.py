import hashlib

from marshmallow import Schema, fields
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.schema import Column, ForeignKey, Index
from sqlalchemy.types import (DateTime, Integer, SmallInteger, BigInteger,
                              String, Boolean, JSON, UnicodeText)

from creamcrape.db.orm import Base

from ..mixin import *


class ArticleSchema(UserDataSchemaMixin, DateTimeSchemaMixin, Schema):
    hash = fields.Str()
    category = fields.Str()
    title = fields.Str()
    text = fields.Str()


class ResponseSchema(UserDataSchemaMixin, DateTimeSchemaMixin, Schema):
    article_hash = fields.Str()
    hash = fields.Str()
    text = fields.Str()


class Article(UserDataMixin, DateTimeMixin, Base):
    __tablename__ = 'article'

    id = Column(BigInteger, primary_key=True)
    hash = Column(String, unique=True, nullable=False)
    category = Column(Integer, nullable=False, default=0)
    title = Column(String, nullable=False, default='')
    text = Column(UnicodeText, nullable=False, default='')
    is_removed = Column(Boolean, nullable=False, default=False)

    responses = relationship('Response',
                             backref=backref('article'),
                             lazy='dynamic')

    def set_hash(self):
        id_hash = hashlib.sha512(
            '{0}:{1}:{2}'.format(
                self.category,
                self.title,
                self.created_at
            ).encode('utf-8'),
        )
        self.hash = id_hash.hexdigest()[:10]


class Response(UserDataMixin, DateTimeMixin, Base):
    __tablename__ = 'response'

    id = Column(BigInteger, primary_key=True)
    hash = Column(String, unique=True, nullable=False)
    article_id = Column(BigInteger,
                        ForeignKey(
                            'article.id',
                            name='fk_article_id',
                            onupdate='CASCADE',
                            ondelete='RESTRICT'),
                        nullable=False
                        )
    article_hash = Column(String, nullable=False, default='')
    text = Column(UnicodeText, default='', nullable=False)
    is_removed = Column(Boolean, nullable=False, default=False)

    def set_hash(self):
        id_hash = hashlib.sha512(
            '{0}:{1}:{2}'.format(
                self.article_id,
                self.user_instant_id,
                self.created_at
            ).encode('utf-8'),
        )
        self.hash = id_hash.hexdigest()[:16]
