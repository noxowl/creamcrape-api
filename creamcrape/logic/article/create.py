from flask import current_app, g
from datetime import datetime

from creamcrape.db.db import session
from creamcrape.common import status_code
from ..enums import CategoryEnum
from .data import Article, Response, ArticleSchema, ResponseSchema


def create_article(payload: dict) -> dict:
    current_app.log.debug(payload)
    article = CreateArticle(**payload)
    article.create()
    if article.result:
        return article.result
    current_app.abort(status_code.bad_request)


def create_response(article_hash: str, payload: dict) -> dict:
    current_app.log.debug(payload)
    payload['article_hash'] = article_hash
    response = CreateResponse(**payload)
    response.create()
    if response.result:
        return response.result
    current_app.abort(status_code.bad_request)


class CreateArticle():
    def __init__(self, **kwargs):
        self.result = {}
        self.error = {}
        self.category = 0
        self.title = ''
        self.text = ''
        self._set_article(kwargs)

    def _set_article(self, kwargs):
        try:
            self.category = CategoryEnum[kwargs['category']].value
            self.title = kwargs['title']
            self.text = kwargs['text']
        except KeyError:
            self.error = {'error': 'key error'}
        except ValueError:
            self.error = {'error': 'value error'}

    def create(self):
        if not self.error:
            schema = ArticleSchema()
            article = Article(
                category=self.category,
                title=self.title,
                text=self.text,
                username=g.user.username,
                email=g.user.email,
                user_instant_id=g.user.instant_id,
                user_credential=g.user.credential,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            article.set_hash()
            with session.begin():
                session.add(article)
            dump, error = schema.dump(article)
            self.result = dump
            if error:
                current_app.log.error(error)
        else:
            current_app.log.error(self.error)


class CreateResponse():
    def __init__(self, **kwargs):
        self.result = {}
        self.error = {}
        self.category = 0
        self.title = ''
        self.text = ''
        self._set_response(kwargs)

    def _set_response(self, kwargs):
        try:
            self.article = session.query(Article).filter_by(hash=kwargs['article_hash']).one_or_none()
            self.text = kwargs['text']
        except KeyError:
            self.error = {'error': 'key error'}
        except ValueError:
            self.error = {'error': 'value error'}

    def create(self):
        if not self.error and self.article:
            schema = ResponseSchema()
            response = Response(
                article_id=self.article.id,
                article_hash=self.article.hash,
                text=self.text,
                username=g.user.username,
                email=g.user.email,
                user_instant_id=g.user.instant_id,
                user_credential=g.user.credential,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            response.set_hash()
            with session.begin():
                session.add(response)
            current_app.log.debug(
                response.__dict__
            )
            dump, error = schema.dump(response)
            self.result = dump
            if error:
                current_app.log.error(error)
        else:
            current_app.log.error(self.error)
