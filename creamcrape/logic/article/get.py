from flask import current_app, g
from datetime import datetime

from creamcrape.db.db import session
from creamcrape.common import status_code

from ..enums import CategoryEnum
from .data import Article, Response, ArticleSchema, ResponseSchema


def get_latest_articles(category_id: str) -> dict:
    current_app.log.debug('find articles')
    articles = session.query(Article).filter_by(category=category_id)\
                                     .order_by(Article.updated_at)\
                                     .all()
    current_app.log.debug(articles)
    if articles:
        article_dumps = []
        for article in articles:
            schema = ArticleSchema()
            dump, error = schema.dump(article)
            current_app.log.debug(dump)
            if error:
                current_app.log.debug(error)
            article_dumps.append(dump)
        return {'articles': article_dumps}
    else:
        current_app.abort(status_code.not_found)


def get_article(article_id: str) -> dict:
    current_app.log.debug('find article')
    article = session.query(Article).filter_by(hash=article_id).one_or_none()
    current_app.log.debug(article)
    if article:
        schema = ArticleSchema()
        dump, error = schema.dump(article)
        current_app.log.debug(dump)
        if error:
            current_app.log.debug(error)
            current_app.abort(status_code.bad_request)
        return {'article': dump}
    else:
        current_app.abort(status_code.not_found)


def get_response(article_hash: str, offset: int, limit: int) -> dict:
    current_app.log.debug('find response')
    responses = []
    article = session.query(Article).filter_by(hash=article_hash).one_or_none()
    if article:
        schema = ResponseSchema()
        if limit:
            resps = article.responses.offset(offset * limit).limit(limit).all()
        else:
            resps = article.responses.all()
        for response in resps:
            dump, error = schema.dump(response)
            if error:
                current_app.log.debug(error)
            responses.append(dump)
        return {'responses': responses}
    else:
        current_app.abort(status_code.not_found)

